import re
import subprocess

class PingError(Exception):
    pass
class HostNotFoundError(Exception):
    pass
class TimeoutError(PingError):
    pass

def ping(host):
    process = subprocess.Popen(['ping', '-n', '1', host], stdout=subprocess.PIPE)
    out, err = process.communicate()
    #print(out)
    code = process.returncode
    if code != 0:
        if b'Request timed out' in out:
            raise TimeoutError(out)
        if b'could not find host' in out:
            raise HostNotFoundError(out)
        raise Exception("Failed ping exit: %d, output: %s" % (code, out))
    
    latency_found = re.findall(rb'time=([0-9]+)ms', out)
    if latency_found:
        return int(latency_found[0])
    #if 'Request timed out' in out or 'subprocess.CalledProcessError' in out:
    raise Exception(out + err)
    
if __name__ == "__main__":
    print(ping('cnn.com'))
    print(ping('8.8.8.8'))
    print(ping('dsafasdfawsefawesadfasdfaweq3w212ascnn.com'))
