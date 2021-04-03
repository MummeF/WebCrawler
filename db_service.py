import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="webcrawler"
)
mycursor = mydb.cursor()


def mapSingleToTuple(single):
    return (single,)


def marks(word):
    word = word.replace("'", "\\'")
    return f"'{word}'"


def addUrls(links):
    links = list(map(mapSingleToTuple, links))
    sql = 'INSERT IGNORE INTO link (url) VALUES (%s)'
    mycursor.executemany(sql, links)
    mydb.commit()


def addWords(url_to_words):
    for element in url_to_words:
        url = element[0]
        saveWords(element[1])
        wordsToId = getWordIds(element[1])
        urlId = getUrlId(url)
        saveWordsToId(urlId, wordsToId)


def getWordInformation(word):
    searchsql = f"select w.*, l.* from word as w join word_to_link as wtl on w.id = wtl.id_word join link as l on wtl.id_link = l.id where w.word like '%{word}%' order by w.id"

    mycursor.execute(searchsql)
    return mycursor.fetchall()


def getUrlId(url):
    searchsql = f"select * from link where url='{url}'"

    mycursor.execute(searchsql)
    return mycursor.fetchone()[0]


def search(word):
    result = []
    wordInformation = getWordInformation(word)
    if(len(wordInformation) > 0):
        print(wordInformation)
        lastword = -1
        lastwordStr = ""
        lastwordlinks = []
        for entry in wordInformation:
            wordId = entry[0]
            wordStr = entry[1]
            linkId = entry[2]
            url = entry[3]
            if lastword != wordId:
                if lastword != -1:
                    result.append((lastword, lastwordStr, lastwordlinks))
                lastwordlinks = [(linkId, url)]
            else:
                lastwordlinks.append((linkId, url))
            lastword = wordId
            lastwordStr = wordStr
        result.append((lastword, lastwordStr, lastwordlinks))
    return result


def saveWords(words):
    sql = 'INSERT IGNORE INTO word (word) VALUES (%s)'
    mycursor.executemany(sql, list(map(mapSingleToTuple, words)))
    mydb.commit()


def saveWordsToId(urlId, wordsToId):
    sql = 'INSERT IGNORE INTO word_to_link (id_word, id_link) VALUES (%s, %s)'
    list_to_insert = []

    for entry in wordsToId:
        list_to_insert.append((entry[0], urlId))

    mycursor.executemany(sql, list_to_insert)
    mydb.commit()


def getWordIds(words):
    if len(words) > 0:
        wordsql = ",".join(list(map(marks, words)))
        searchsql = f'select * from word where word in ({wordsql})'
        searchsql = searchsql.replace("\n", "")
        print(searchsql)
        mycursor.execute(searchsql)
        return mycursor.fetchall()
    return []
