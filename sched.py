
#
# def job_2():
#     print("Job2 실행: ", "| [time] "
#           , str(time.localtime().tm_hour) + ":"
#           + str(time.localtime().tm_min) + ":"
#           + str(time.localtime().tm_sec))
#
# sched = BackgroundScheduler()
# sched.start()
#
# sched.add_job(job_2, 'interval', seconds=3, id="test_2")

# from apscheduler.schedulers.background import BackgroundScheduler
import time
import schedule
def job_2(input_num):
    print("Job2 실행: ", "| [time] " ,input_num)

input_nums = input('input number')
job_id1 = schedule.every(1).seconds.do(job_2,input_nums)
count =0
while count < 5:

    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()

    time.sleep(1)

    count = count +1

    # if count > 3:
    #     schedule.cancel_job(job_id1)

print('Job is done!')