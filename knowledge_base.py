#知识库
import os
from fileinput import filename
from importlib.metadata import metadata

import data
from langchain_community.tools.connery import service

import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import os
os.environ["DASHSCOPE_API_KEY"] = "sk-ws-H.YMPHLXP.a23S.MEUCIQCT3-ppt2-v37Js2cdPaF0isWC_NVkwA9neUNUPC6rIiwIgHpEiUmcIqtgHg_yB7o7wTPtv4nj1xLyvh12x_9vTAnw"




def check_md5(md5_str:str):
    '''检查传入的md字符串是否已经被处理过了
        return false未处理，true已处理'''
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()  #处理字符串前后的空格和回车
            if line == md5_str:
                return True

        return False



def save_md5(md5_str:str):
    '''记录保存'''
    with open(config.md5_path,'w',encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str:str,encoding='utf-8'):

    '''字符串转为md5'''

    #将字符串转化为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)

    #创建md5对象
    md5_obj = hashlib.md5()  #得到md5对象
    md5_obj.update(str_bytes)  #更新内容
    md5_hex = md5_obj.hexdigest()  #得到md5的十六进制字符串

    return md5_hex
print("已读取 API Key：", bool(os.getenv("DASHSCOPE_API_KEY")))

class KnowledgeBaseService(object):

    def __init__(self):
        #如果文件夹不存在就创建，存在就跳过
        os.makedirs(config.persist_directory, exist_ok=True)

        self.chroma = Chroma(
            collection_name=config.collection_name,  #数据库表名
            embedding_function=DashScopeEmbeddings(model='text-embedding-v3'),
            persist_directory=config.persist_directory,  #数据库本地文件夹
        )   #向量存储的实例chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  #分割的文本段最大长度
            chunk_overlap=config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators=config.separators,   #自然段落划分的符号
            length_function=len,  #使用python自带的len函数做长度统计的依据
        ) #文本分割器对象

    def upload_by_str(self,data : str,filename):
        '''进行向量化，存入向量数据库中'''
        #先得到传入字符串的md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return '[跳过]内容已存在知识库'

        if len(data) > config.max_split_char_number:
            knowledge_chunks :list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks =[data]

        metadata = {
            'source': filename,
            #2025-01-02
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator':'小曹',
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return'[成功]内容已经成功载入向量库'



if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str('周杰伦222','testfile')
    print(r)