import sqlite3 as lite 

def in_db(repo_uuid):
    con = lite.connect('classnotes.db')

    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Keys WHERE Repo_UUID='{0}'".format(repo_uuid))
        
        row = cur.fetchone()
        print row
        
        if row == None: return False
        else: return True


def add_bitbucket_token_to_db(repo_uuid, ACCESS_TOKEN):   
    
    with lite.connect('classnotes.db') as con:
        
        cur = con.cursor()
        
        cur.execute("SELECT Repo_UUID FROM Keys WHERE Repo_UUID='{0}'".format(repo_uuid))
        
        row = cur.fetchone()
        
        if row == None:
            cur.execute("INSERT INTO Keys(Repo_UUID, Bitbucket_Key) VALUES ('{0}', '{1}')".format(repo_uuid, ACCESS_TOKEN))
        else:
            cur.execute("UPDATE Keys SET Bitbucket_Key='{0}' WHERE Repo_UUID='{1}'".format( ACCESS_TOKEN, repo_uuid ))

    return True


    
def add_onenote_token_to_db(repo_uuid, ACCESS_TOKEN):
    con = lite.connect('classnotes.db')

    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Keys WHERE Repo_UUID = '{0}'".format(repo_uuid))
        
        row = cur.fetchone()
        if row == None:
            cur.execute("INSERT INTO Keys(Repo_UUID, OneNote_Key) VALUES ('{0}', '{1}')".format(repo_uuid, ACCESS_TOKEN))
        else:
            cur.execute("UPDATE Keys SET OneNote_Key='{0}' WHERE Repo_UUID='{1}'".format(ACCESS_TOKEN, repo_uuid))
    
    return True
    
    
def get_token(repo_uuid, service):
    
    with lite.connect('classnotes.db') as con:
        cur = con.cursor()
        
        try:
            cur.execute("SELECT {0}_Key FROM Keys WHERE Repo_UUID = '{1}'".format(service, repo_uuid))
        except Exception, e:
            print e.args[0]
            
        row = cur.fetchone()
        
        if row == None:
            return None
        else:
            return row[0]