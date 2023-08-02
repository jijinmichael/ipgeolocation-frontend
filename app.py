from flask import Flask, render_template,  make_response
import requests
import re
import os

app = Flask(__name__)



@app.route('/',strict_slashes=False)
@app.route('/ip',strict_slashes=False)
@app.route('/ip/<ip>',strict_slashes=False)
def index(ip=None):
  
  if ip != None:
        
    pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    valid_ip = pattern.match(ip.strip())
    
    if valid_ip:
        
      api_url = "http://{}:{}/ip/{}".format(api_server,api_server_port,ip) 
      response = requests.get(url=api_url)
      geodata = response.json()
      continent_name = geodata['continent_name']
      continent_code = geodata['continent_code']
      country_name = geodata['country_name']
      isp = geodata['isp']
      cached = geodata['cached']
      apiServer = geodata['apiServer'] 
   
      return render_template('index.html',
                         continent_name=continent_name,
                         continent_code=continent_code,
                         country_name=country_name,
                         isp=isp,
                         cached=cached,
                         host=hostname,
                         apiServer=apiServer,
                         hostname=hostname
                         )

    else:
        
      return render_template('error.html')

  else:
       
    return render_template('error.html')
    
  
@app.route('/status',strict_slashes=False)
def check_status():
  return make_response("",200)


if __name__ == "__main__":
  
  hostname = os.getenv("HOSTNAME","none")
  api_server = os.getenv("API_SERVER",None)
  api_server_port = os.getenv("API_SERVER_PORT",None)
  app_port = os.getenv('APP_PORT',"8080") 
  app.run(port=app_port,host="0.0.0.0",debug=True)
