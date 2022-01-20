import asyncio


async def main():
    task=asyncio.create_task(foo("ololo"))
    for j in range(10):
        print("azaza")
        await asyncio.sleep(2)

async def foo(text):
    for i in range(10):
        print(text)
        await asyncio.sleep(1)
asyncio.run(main())