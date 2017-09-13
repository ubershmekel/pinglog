import sys
import re
import subprocess

class PingError(Exception):
    pass
class HostNotFoundError(Exception):
    pass
class TimeoutError(PingError):
    pass

_platform = sys.platform
if _platform == "linux" or _platform == "linux2":
    # linux
    count_param = '-c'
    latency_pattern = 'time=([0-9\.]+) ms'
elif _platform == "darwin":
    # OS X, dunno if this is correct
    count_param = '-c'
    latency_pattern = 'time=([0-9\.]+)\s*ms'
elif _platform == "win32":
    # Windows...
    count_param = '-n'
    latency_pattern = 'time[=<]([0-9]+)ms'

def ping(host):
    process = subprocess.Popen(['ping', count_param, '1', host], stdout=subprocess.PIPE)
    out, err = process.communicate()
    #print(out)
    code = process.returncode
    if code != 0:
        if b'Request timed out' in out:
            raise TimeoutError(out)
        if b'could not find host' in out:
            raise HostNotFoundError(out)
        raise Exception("Failed ping exit: %d, output: %s" % (code, out))
    
    latency_found = re.findall(latency_pattern, out.decode('utf-8'))
    if latency_found:
        return float(latency_found[0])
    #if 'Request timed out' in out or 'subprocess.CalledProcessError' in out:
    raise Exception("Failed to parse ping output '%s' '%s'" % (out, err))
    
if __name__ == "__main__":
    print(ping('cnn.com'))
    print(ping('8.8.8.8'))
    print(ping('dsafasdfawsefawesadfasdfaweq3w212ascnn.com'))
