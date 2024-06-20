
**MySQLログイン**
<br>``` mysql -u root -p ```
<br>```PW:root ```

**python仮想環境実行時ディレクトリ**
<br>```/home/ubuntu/attendance```

**仮想環境入りコマンド**
<br>```source jobpit_env/bin/activate```

**マイグレーション時のディレクトリ**
<br>```/home/ubuntu/attendance/jobpit```


[起動手順]
<br>1.仮想環境に入る
<br>2.manage.pyのあるディレクトリで下記を実行
<br> ```gunicorn --bind 0.0.0.0:8000 jobpit.wsgi:application ```
<br> -Dのオプションでバックグラウンドで稼働可<br>


※プロセス終了コード<br>
``` ps aux | grep gunicorn ```<br>
``` kill {プロセスid} ```