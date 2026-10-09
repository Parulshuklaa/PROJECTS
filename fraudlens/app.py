from pathlib import Path
import io, json, sqlite3, os
from datetime import datetime, timezone
import pandas as pd
from flask import Flask, request, jsonify, render_template
from ml import Engine, FEATURES

def create_app(db_path=None):
    app=Flask(__name__)
    app.config['MAX_CONTENT_LENGTH']=1024*1024
    db_path=db_path or os.environ.get('FRAUDLENS_DB',str(Path(__file__).parent/'transactions.db'))
    engine=Engine()
    def connect():
        con=sqlite3.connect(db_path); con.row_factory=sqlite3.Row; return con
    with connect() as con:
        con.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, created TEXT NOT NULL, input TEXT NOT NULL, result TEXT NOT NULL, feedback TEXT)')
    def save(data,result):
        with connect() as con:
            cur=con.execute('INSERT INTO transactions(created,input,result) VALUES(?,?,?)',(datetime.now(timezone.utc).isoformat(),json.dumps(data),json.dumps(result)))
            return cur.lastrowid
    @app.get('/')
    def home(): return render_template('index.html')
    @app.get('/api/health')
    def health(): return jsonify(status='ok',models='loaded')
    @app.get('/api/metrics')
    def metrics(): return jsonify(engine.b['report'])
    @app.get('/api/transactions')
    def history():
        with connect() as con: rows=con.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 200').fetchall()
        return jsonify([{'id':r['id'],'created':r['created'],'input':json.loads(r['input']),'result':json.loads(r['result']),'feedback':r['feedback']} for r in rows])
    @app.post('/api/predict')
    def predict():
        try:
            data=request.get_json(silent=True); result=engine.score(data)
            normalized={f:float(data[f]) for f in FEATURES}
            return jsonify(id=save(normalized,result),**result)
        except ValueError as e: return jsonify(error=str(e)),400
    @app.post('/api/batch')
    def batch():
        if 'file' not in request.files: return jsonify(error='CSV file required'),400
        try:
            df=pd.read_csv(request.files['file'])
            if not 1<=len(df)<=500: raise ValueError('Use 1–500 rows')
            if not set(FEATURES)<=set(df.columns): raise ValueError('Missing required feature columns')
            rows=df[FEATURES].to_dict('records')
            results=[engine.score(r) for r in rows] # Validate entire batch before writing.
            with connect() as con:
                for data,result in zip(rows,results):
                    con.execute('INSERT INTO transactions(created,input,result) VALUES(?,?,?)',(datetime.now(timezone.utc).isoformat(),json.dumps(data),json.dumps(result)))
            return jsonify(count=len(results),results=results)
        except (ValueError,pd.errors.ParserError,pd.errors.EmptyDataError,UnicodeError) as e: return jsonify(error=str(e)),400
    @app.post('/api/transactions/<int:tid>/feedback')
    def feedback(tid):
        body=request.get_json(silent=True)
        label=body.get('label') if isinstance(body,dict) else None
        if label not in ('fraud','legitimate'): return jsonify(error='label must be fraud or legitimate'),400
        with connect() as con:
            cur=con.execute('UPDATE transactions SET feedback=? WHERE id=?',(label,tid))
            if not cur.rowcount: return jsonify(error='Transaction not found'),404
        return jsonify(status='saved')
    @app.errorhandler(413)
    def too_large(e): return jsonify(error='Upload exceeds 1 MB'),413
    return app

if __name__=='__main__': create_app().run(host='127.0.0.1',port=5000,debug=False)
