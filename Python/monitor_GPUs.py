#coding:utf-8
import os, time, sys, re
import argparse

CLEAR_TO_END = "\033[K"
UP_ONE_LINE = "\033[F"

parser = argparse.ArgumentParser(description='Monitor system GPUs usage information until it could be used to run your programs, then call them.')
parser.add_argument('-c','--cmd', type=str, default='',
                    help='the scripts cmd to call to run.')
parser.add_argument('-i', '--interval', type=float, default=2,
                    help='a second arg for update interval time(s), default is 2')
parser.add_argument('-g','--is_multi_gpu', action="store_false", default=True,
                    help='whether to use multi gpus if avilable, default is True.')
parser.add_argument('-t', '--threshold', type=float, default=0.20,
                    help='percentage than which determine [cmd] to run if usage of gpus less, default is 0.20')
args = parser.parse_args()

def print_state(states):
    delta_line = len(states)
    sys.stdout.write(UP_ONE_LINE * delta_line if delta_line > 0 else '')
    for i in range(delta_line):
        sys.stdout.write('\r' + CLEAR_TO_END)
        sys.stdout.write('\rGPU: '+str(i)+' has been used of '+str(states[i]*100)+'%')
        sys.stdout.write('\n')
        # sys.stdout.flush()

def check(states, threshold=0.20):
    x = []
    for i in range(len(states)):
        if states[i]<threshold:
            x.append(i)
    return x

def monitor(env_cmd=None, interval=2, is_multi_gpu=True, threshold=0.20):
    assert env_cmd is not None, 'You must assign a command to run!'
    try:
        r = os.popen('nvidia-smi -L')
    except:
        print('It seems something wrong!\nPlease check and fix it!')

    GPU_list = r.readlines()
    # If non GPU, exit with Error.
    assert not len(GPU_list)==0, 'Your system didn''t have NVIDIA GPUs!'
    # Remove the jump lines' effect.
    print('\n'*len(GPU_list))
    while True:
        r = os.popen('nvidia-smi')

        GPU_state = r.readlines()

        k = 0
        states = []
        for i in range(len(GPU_list)):
            matchtxt = '([\d]*)MiB /  ?([\d]*)MiB'
            # print(GPU_state[8+k])
            info = re.findall(matchtxt,GPU_state[8+k])
            # print(info)
            states.append(float(info[0][0])/float(info[0][1]))
            k += 3
        print_state(states)
        x = check(states, threshold) # return ids list
        if not len(x) == 0:
            xs = ''
            sys.stdout.write('\n\n')
            for i in x:
                print('GPU: '+str(i)+' is could be use now!\n')
                xs += (str(i)+',')
            xs = xs[:-1] # remove the last ,
            if is_multi_gpu and (len(x)>1 or len(GPU_list)==1):
                print('GPU: '+xs+' could has been OK!\n')
                # Call your scripts.
                os.system(env_cmd+' '+xs)
            elif is_multi_gpu and len(x)==1:
                sys.stdout.write(UP_ONE_LINE*2)
                continue
            else:
                # Call your scripts here with x[0]
                print('GPU: '+str(x[0])+' could has been OK!\n')
                os.system(env_cmd+' '+str(x[0]))
            break
        time.sleep(interval)

if __name__ == '__main__':
    assert not args.cmd == '', 'please assign cmd scripts'
    print(args)
    monitor(env_cmd=args.cmd, interval=args.interval, is_multi_gpu=args.is_multi_gpu, threshold=args.threshold)
