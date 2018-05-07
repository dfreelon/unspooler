from collections import defaultdict
import re
import requests
import time
import urllib3

short_list = ["/bit.ly/","/ow.ly/","/goo.gl/","/buff.ly/","/ift.tt/","/ln.is/","/trib.al/","/dlvr.it/","/tinyurl.com/","/shar.es/","/j.mp/","/owl.li/","/dld.bz/","/fw.to/","/is.gd/"]
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

def handle_link_err(e,u):
    ename = type(e).__name__
    print(ename+":",e,"with",u)
    return u

def save_data(datum,save_file):
    try:
        with open(save_file,"a") as out:
            out.write(','.join(datum)+'\n')
    except (UnicodeDecodeError,UnicodeEncodeError):
        pass

def unspool(txt_data,short_domains=short_list,resume_dict=None,save_file="",save_dups=False,keep_query_strings=['youtube.com'],verbose=True):
    if type(txt_data) is str:
        txt_data = [txt_data]
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    data_len = len(txt_data)
    unspooled_output = {}
    if resume_dict is None:
        unspooled_output['urls'] = {}
        unspooled_output['ct'] = defaultdict(int)
        unspooled_output['skip_urls'] = []
        start_index = 0
        
    else:
        try:
            unspooled_output['urls'] = resume_dict['urls']
            unspooled_output['ct'] = resume_dict['ct']
            unspooled_output['skip_urls'] = resume_dict['skip_urls']
            start_index = resume_dict['index']
            print("Unspool resume attempt successful. Starting in 3 secs...")
            time.sleep(3)
        except Exception as e:
            raise TypeError("You attempted to resume unspooling with an invalid object (should be a dict). Try again, maybe?")
    
    for x,txt_string in enumerate(txt_data[start_index:]):
        url_list = [''.join(u) for u in re.findall(r'(http)(s?)(://.+?)(?:\s|$)',txt_string)]
        url_list = [re.sub("[^a-zA-Z0-9\-_:;/.?#@%&+=,~]","",i) for i in url_list]
        unspooled_output['curr_urls'] = {}
        unspooled_output['index'] = x + start_index
           
        for n,u in enumerate(url_list):
            if "?" in u and not any(d in u for d in keep_query_strings):
                u = u[:u.find("?")]
            if any(d in u for d in short_domains) and u not in unspooled_output['skip_urls']:
                if u in unspooled_output['urls']:
                    datum = (u,unspooled_output['urls'][u])
                    unspooled_output['ct'][u] += 1
                    unspooled_output['curr_urls'][u] = unspooled_output['urls'][u]
                    if save_dups == True and save_file != "":
                        save_data(datum,save_file)
                        #continue
                    yield unspooled_output 
                else:
                    try:
                        r = requests.head(u,allow_redirects=False,headers=headers,timeout=20)
                        save_url = r.headers['location']
                    except KeyError:
                        try:
                            r = requests.head(u,timeout=20)
                            save_url = r.headers['location']
                            while any(d in r.headers['location'] for d in short_domains):
                                r = requests.head(r.headers['location'],timeout=20)
                                save_url = r.headers['location']
                        except Exception as e:
                            unspooled_output['skip_urls'].append(handle_link_err(e,u))
                            continue
                    except (KeyboardInterrupt, SystemExit):
                        raise
                    except Exception as e:
                        unspooled_output['skip_urls'].append(handle_link_err(e,u))
                        continue
                    if "?" in save_url and not any(d in save_url for d in keep_query_strings):
                        save_url = save_url[:save_url.find("?")]
                    datum = (u,save_url)
                    unspooled_output['urls'][u] = save_url
                    unspooled_output['curr_urls'][u] = save_url
                    unspooled_output['ct'][u] += 1
                    
                    if save_file != "":
                        save_data(datum,save_file)
                    yield unspooled_output
        if verbose == True:               
            progress = round(100*(unspooled_output['index']+1)/data_len,3)
            print("Text",unspooled_output['index']+1,"complete (",progress,"% completed.)")

def unspool_easy(txt_data,short_domains=short_list,resume_dict=None,save_file="",save_dups=False,keep_query_strings=['youtube.com'],verbose=True):
    unspool_dict = {}
    for unsp in unspool(txt_data,short_domains,resume_dict,save_file,save_dups,keep_query_strings,verbose):
        unspool_dict.update(unsp)
    return unspool_dict
    