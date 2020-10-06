#case1 
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
'''
started at 15:00:36
hello
world
finished at 15:00:39

可以看到，总的执行时间是3秒
'''



#case2 
import asyncio
import time

async def say_after(delay,what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(
        say_after(1,'hello')
    )

    task2 = asyncio.create_task(
        say_after(2,'world')
    )
    print(f"started at {time.strftime('%X')}")
    await task2
    await task1
    print(f"finished at {time.strftime('%X')}")
asyncio.run(main())
#执行结果
'''
started at 14:51:03
hello
world
finished at 14:51:05

可以看到上述总的执行时间是2秒

'''