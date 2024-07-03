import sqlite3
import json

class AutoComplete:
    """
    它通过构建一个`WordMap`来工作，该`WordMap`存储单词到单词跟随者计数
    ----------------------------
    例如，要训练以下语句：
    
    It is not enough to just know how tools work and what they worth,
    we have got to learn how to use them and to use them well.
    And with all these new weapons in your arsenal, we would better
    get those profits fired up

    我们创建以下内容：
    {   It: {is:1}
        is: {not:1}
        not: {enough:1}
        enough: {to:1}
        to: {just:1, learn:1, use:2}
        just: {know:1}
        .
        .
        profits: {fired:1}
        fired: {up:1}
    }
    因此，“to”的单词补全将是“use”。
    为了优化，我们使用另一个存储`WordPrediction`来保存每个单词的预测
    """

    def __init__(self):
        """
        返回 - None
        输入 - None
        ----------
        - 初始化数据库。我们使用sqlite3
        - 检查表是否存在，如果不存在则创建它们
        - 维护类级别访问数据库连接对象
        """
        self.conn = sqlite3.connect("autocompleteDB.sqlite3", autocommit=True)
        cur = self.conn.cursor()
        res = cur.execute("SELECT name FROM sqlite_master WHERE name='WordMap'")
        tables_exist = res.fetchone()

        if not tables_exist:
            self.conn.execute("CREATE TABLE WordMap(name TEXT, value TEXT)")
            self.conn.execute('CREATE TABLE WordPrediction (name TEXT, value TEXT)')
            cur.execute("INSERT INTO WordMap VALUES (?, ?)", ("wordsmap", "{}",))
            cur.execute("INSERT INTO WordPrediction VALUES (?, ?)", ("predictions", "{}",))

    def train(self, sentence):
        """
        返回 - 字符串
        输入 - str: 一个称为句子的单词字符串
        ----------
        训练句子。它通过创建当前单词到下一个单词及其每次出现的计数的映射来实现
        - 接受句子并将其拆分为单词列表
        - 检索单词映射和预测映射
        - 一起创建单词映射和预测映射
        - 将单词映射和预测映射保存到数据库
        """
        cur = self.conn.cursor()
        words_list = sentence.split(" ")

        words_map = cur.execute("SELECT value FROM WordMap WHERE name='wordsmap'").fetchone()[0]
        words_map = json.loads(words_map)

        predictions = cur.execute("SELECT value FROM WordPrediction WHERE name='predictions'").fetchone()[0]
        predictions = json.loads(predictions)

        for idx in range(len(words_list)-1):
            curr_word, next_word = words_list[idx], words_list[idx+1]
            if curr_word not in words_map:
                words_map[curr_word] = {}
            if next_word not in words_map[curr_word]:
                words_map[curr_word][next_word] = 1
            else:
                words_map[curr_word][next_word] += 1

            # 检查补全单词与下一个单词
            if curr_word not in predictions:
                predictions[curr_word] = {
                    'completion_word': next_word,
                    'completion_count': 1
                }
            else:
                if words_map[curr_word][next_word] > predictions[curr_word]['completion_count']:
                    predictions[curr_word]['completion_word'] = next_word
                    predictions[curr_word]['completion_count'] = words_map[curr_word][next_word]

        words_map = json.dumps(words_map)
        predictions = json.dumps(predictions)

        cur.execute("UPDATE WordMap SET value = (?) WHERE name='wordsmap'", (words_map,))
        cur.execute("UPDATE WordPrediction SET value = (?) WHERE name='predictions'", (predictions,))
        return("训练完成")

    def predict(self, word):
        """
        返回 - 字符串
        输入 - 字符串
        ----------
        返回输入单词的补全单词
        - 接受一个单词
        - 检索预测映射
        - 返回输入单词的补全单词
        """
        cur = self.conn.cursor()
        predictions = json.loads(cur.execute("SELECT value FROM WordPrediction WHERE name='predictions'").fetchone()[0])
        return predictions.get(word.lower(), {}).get('completion_word', None)



if __name__ == "__main__":
    input_ = "It is not enough to just know how tools work and what they worth,\
              we have got to learn how to use them and to use them well. And with\
              all these new weapons in your arsenal, we would better get those profits fired up"
    ac = AutoComplete()
    ac.train(input_)
    print(ac.predict("to"))