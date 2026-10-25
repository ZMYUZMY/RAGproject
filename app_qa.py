import streamlit as st
import time
from rag import RagService
import config_data as config


#标题
st.title('智能客服')
st.divider()       #分隔符

rag_service = RagService(embedding=config.embedding_model_name)

if 'message' not in st.session_state:
    st.session_state['message'] = [{'role':'assistant','content':'你好，有什么可以帮助你'}]

if 'rag' not in st.session_state:
    st.session_state['rag'] = RagService(embedding=config.embedding_model_name)

for message in st.session_state['message']:
    st.chat_message(message['role']).write(message['content'])

#在页面最下面提供用户输入栏
prompt = st.chat_input()

if prompt:

    # 在页面输出用户的提问
    st.chat_message('user').write(prompt)
    st.session_state['message'].append({'role':'user','content':prompt})

    ai_res_list = []
    with st.spinner('AI思考中...'):
        #time.sleep(1)
        res_stream = st.session_state['rag'].chain.stream({'input':prompt},config.session_config)

        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message('assistant').write_stream(res_stream)
        st.session_state['message'].append({'role': 'assistant', 'content':res_stream})
