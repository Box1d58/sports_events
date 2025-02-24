import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.run_daily import run_daily

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_daily, trigger=CronTrigger(hour=17, minute=30))
    scheduler.start()

    print("Планировщик запущен. Ожидаем задачи...")

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        print("Остановка планировщика")
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
