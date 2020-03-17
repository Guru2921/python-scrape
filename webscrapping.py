#Beatiful Soup - To parse the html
from bs4 import BeautifulSoup
#urllib.request - to make http request
from urllib.request import Request, urlopen
#To remove any language special characters
import unicodedata
# EMAIL library
import smtplib
# URL parser
from urllib.parse import urlparse
from urllib.parse import parse_qs
# mysql connector
import mysql.connector
from mysql.connector import Error
# ENV file
from dotenv import load_dotenv
# env
from os import environ
# time
import time

def get_employment_type(endpoint):
	if endpoint[0] == '/' and endpoint[1] == '/':
		endpoint = "https:" + endpoint
	req = Request(endpoint, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'lxml')
	info = soup.find("li", class_="posInfo posInfo--employmentType")
	job_type = ""
	if  info is not None:
		job_type = info.find('div', class_="posInfo__Value").text.strip()
	return job_type

def get_jobs(soup):
	job_array = []
	jobs = soup.find_all("li", class_='BambooHR-ATS-Jobs-Item')
	for job in jobs:
		job_title = job.find('a').text.strip()
		job_url = job.find('a').attrs['href'].strip()
		job_type = get_employment_type(job_url)
		url = urlparse(job_url)
		params = parse_qs(url.query)
		job_id = params['id'][0]
		job_location = job.find('span', class_="BambooHR-ATS-Location").text.strip()
		job_array.append({
			'job_title' : job_title,
			'job_url' : job_url,
			'job_id' : job_id,
			'job_location' : job_location,
			'job_type' : job_type
		})
		print(job_id + " has been parsed!")
	return job_array

def save_jobs_to_mysql(jobs):
	try:
		db_host = environ.get("DB_HOST")
		db_user = environ.get("DB_USER")
		db_password = environ.get("DB_PASSWORD")
		db_name = environ.get("DB_NAME")
		connection = mysql.connector.connect(host=db_host,
											database=db_name,
											user=db_user,
											password=db_password)
		if connection.is_connected():
			for job in jobs:
				try:
					cursor = connection.cursor()
					mySql_insert_query = """INSERT INTO jobs (ID, job_title, url, location, employment_type) 
											VALUES
											(%s, %s, %s, %s, %s)
											ON DUPLICATE KEY UPDATE
											job_title=%s,url=%s,location=%s,employment_type=%s
											"""
					cursor.execute(mySql_insert_query, (job['job_id'], job['job_location'], job['job_url'], job['job_location'], job['job_type'], job['job_location'], job['job_url'], job['job_location'], job['job_type']))
					connection.commit()
					print(job['job_id'] + " has been updated!")
				except Error as e:
					print("Error while updating the table!", e)
	except Error as e:
		print("Error while connecting to MySQL", e)
	finally:
		if (connection.is_connected()):
			cursor.close()
			connection.close()
			print("MySQL connection is closed")
def run():
	start_time = time.time()
	endpoint = "https://sohodragon.bamboohr.com/jobs/embed2.php"
	req = Request(endpoint, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	soup = BeautifulSoup(webpage, 'lxml')
	jobs_ = get_jobs(soup)
	# print(jobs_)
	save_jobs_to_mysql(jobs_)
	elapsed_time = time.time() - start_time
	print("Elapsed Time: ", elapsed_time)
	return jobs_

if __name__ == '__main__':
	load_dotenv()
	run()