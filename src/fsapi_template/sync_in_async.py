# 为了保证 FastAPI 程序的高效运行
# 代码应该保持非阻塞
# 对于无法 await 的代码，需要包装到线程中运行
# python 内置的 asyncio.to_thread 可以用来做这个事情的
# 但是没有优雅的编辑器补全支持和错误提示
# 为了如原生 async def 般调用阻塞 def，
# 可以使用 FastAPI 同作者开发的 Asyncer
# 文档参见： https://asyncer.tiangolo.com/tutorial/
# 下面是一个代码示例


# import asyncio
# import time

# import anyio
# from asyncer import asyncify


# def do_sync_work(name: str):
#     time.sleep(1)
#     return f"Hello, {name}"


# async def main():
#     # 可以不依赖第三方库
#     a = await asyncio.to_thread(do_sync_work, name="World")
#     print(a)


# async def main():
#     # 此处传参时，可以获得编辑器自动补全
#     # 编辑器也可以推断出返回类型， 比如 message 是一个数据模型
#     message = await asyncify(do_sync_work)(name="World")

#     print(message)


# anyio.run(main)
