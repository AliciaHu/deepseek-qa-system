# 在src/utils/中添加monitor.py
import tracemalloc
import time

def memory_monitor(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = time.time()
        
        result = func(*args, **kwargs)
        
        snapshot = tracemalloc.take_snapshot()
        stats = snapshot.statistics('lineno')
        print(f"[内存] 峰值占用：{stats[0].size/1e6:.1f}MB")
        print(f"[耗时] {time.time()-start_time:.2f}s")
        tracemalloc.stop