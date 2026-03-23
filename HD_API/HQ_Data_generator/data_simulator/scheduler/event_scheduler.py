import scheduler
import time

scheduler.every(5).seconds.do(run_sales_flow)

while True:
    scheduler.run_pending()
    time.sleep(1)

    