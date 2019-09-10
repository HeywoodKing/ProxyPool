
import sys
import io
from proxypool.scheduler import Scheduler

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except KeyboardInterrupt as ex:
        print('用户终止了代理池运行，{}'.format(ex))
    except Exception as ex:
        print('代理池运行异常，{}'.format(ex))
        main()


if __name__ == '__main__':
    main()
