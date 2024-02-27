import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import testfetchanddownload2  # 用于下载网站数据


async def wakeup_job():
    print("Job started to wakeup")
    await testfetchanddownload2.download_website_data()  # 调用异步下载函数
    print("Job completed")


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(wakeup_job, 'interval', seconds=10)  # 注册异步任务

    scheduler.start()
    print("Scheduler started")

    try:
        while True:
            await asyncio.sleep(0)  # 释放异步时间片
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())