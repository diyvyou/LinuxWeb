import psutil

def Push():
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)

    # 获取内存使用率
    memory_usage = psutil.virtual_memory().percent

    # 获取磁盘使用率
    disk_usage = psutil.disk_usage('/').percent

    # 输出结果
    sCpu = "CPU使用率:{}%".format(cpu_usage)
    sMemory = "内存使用率：{}%".format(memory_usage)
    sDisk = "磁盘使用率：{}%".format(disk_usage)
    return sCpu,sMemory,sDisk