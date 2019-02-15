#~ this script will fetch data from the sierra postgresql database and
#~ fill a local database.

import configparser
import sqlite3
import psycopg2
import psycopg2.extras
import csv
import os
from random import randint
from datetime import datetime, date
import ftplib

# debug
# import pdb

class App:

	def __init__(self):

		self.d = date.today()
		#~ open the config file, and parse the options into local vars
		config = configparser.ConfigParser()
		config.read('config.ini')

		 # get the output path from the config
		self.output_path = config['misc']['output_path']
		print('output_path: {}'.format(self.output_path))
		if not os.path.exists(self.output_path):
			os.sys.exit('ERROR: output path doesn\'t exist ... exiting')

		# set the filenames for the output csv files
		self.csv_bib_file_name = os.path.join(
			self.output_path,
			self.d.strftime("%Y-%m-%d-plch-bib.csv")
		)
		self.csv_item_file_name = os.path.join(
			self.output_path,
			self.d.strftime("%Y-%m-%d-plch-item.csv")
		)
		self.csv_hold_file_name = os.path.join(
			self.output_path,
			self.d.strftime("%Y-%m-%d-plch-hold-snapshot.csv")
		)

		# get the FTP info from the config
		self.ftp_host = config['ftp']['ftp_host']
		self.ftp_username = config['ftp']['ftp_username']
		self.ftp_password = config['ftp']['ftp_password']

		# the salt used for encoding the bib record id (make sure the salt is the same going forward, or we won't be able to id unique bibs)
		self.salt = config['misc']['salt']

		# the remote database connection
		self.db_connection_string = config['db']['connection_string']
		self.pgsql_conn = None

		# the local database connection
		self.local_db_connection_string = os.path.join(self.output_path, config['local_db']['connection_string'])
		self.sqlite_conn = None

		# the number of rows to iterate over
		self.itersize = int(config['db']['itersize'])

		# open the database connections
		self.open_db_connections()

		# create the table if it doesn't exist
		self.create_local_table()

		# create the temp table, and fill it with any local IDs (if there are any)
		self.create_remote_temp_tables()

		# fill the local database
		self.fill_local_db()

		# FTP the output
		self.ftp_session = ftplib.FTP(
			host=self.ftp_host, user=self.ftp_username, passwd=self.ftp_password, timeout=600
		)

		# upload bib
		print('uploading bib file: {}...'.format(self.csv_bib_file_name))
		file = open(self.csv_bib_file_name, 'rb')
		self.ftp_session.storbinary('STOR ' + self.csv_bib_file_name, file)
		print('done. file size on FTP: {}'.format(self.ftp_session.size(self.csv_bib_file_name)))
		file.close()

		# upload item
		print('uploading item file: {}...'.format(self.csv_item_file_name))
		file = open(self.csv_item_file_name, 'rb')
		self.ftp_session.storbinary('STOR ' + self.csv_item_file_name, file)
		print('done. file size on FTP: {}'.format(self.ftp_session.size(self.csv_item_file_name)))
		file.close()

		# upload hold
		print('uploading hold file: {}...'.format(self.csv_hold_file_name))
		file = open(self.csv_hold_file_name, 'rb')
		self.ftp_session.storbinary('STOR ' + self.csv_hold_file_name, file)
		print('done. file size on FTP: {}'.format(self.ftp_session.size(self.csv_hold_file_name)))
		file.close()

		self.ftp_session.quit()


	#~ the destructor
	def __del__(self):
		self.sqlite_conn.commit()
		self.close_connections()
		print("done.")


	def open_db_connections(self):
		#~ connect to the sierra postgresql server
		try:
			self.pgsql_conn = psycopg2.connect(self.db_connection_string)

		except psycopg2.Error as e:
			print("unable to connect to sierra database: %s" % e)

		#~ connect to the local sqlite database
		try:
			self.sqlite_conn = sqlite3.connect(self.local_db_connection_string)
		except sqlite3.Error as e:
			print("unable to connect to local database: %s" % e)


	def close_connections(self):
		print("closing database connections...")
		if self.pgsql_conn:
			if hasattr(self.pgsql_conn, 'close'):
				print("closing pgsql_conn")
				self.pgsql_conn.close()
				self.pgsql_conn = None

		if self.sqlite_conn:
			if hasattr(self.sqlite_conn, 'close'):
				print("closing sqlite_conn")
				self.sqlite_conn.close()
				self.sqlite_conn = None


	def create_local_table(self):
		cursor = self.sqlite_conn.cursor()
		
		# create the bib table if it doesn't exist
		sql = """
		CREATE TABLE IF NOT EXISTS "bib" ( `bib_record_num` INTEGER, `bib_record_id` INTEGER, `control_numbers` TEXT, `creation_date` TEXT, `record_last_updated` TEXT, `isbn` TEXT, `best_author` TEXT, `best_author_norm` TEXT, `best_title` TEXT, `best_title_norm` TEXT, `publisher` TEXT, `publish_year` INTEGER, `bib_level_callnumber` TEXT, `indexed_subjects` TEXT, `is_deleted` INTEGER DEFAULT 0, PRIMARY KEY(`bib_record_id`) )
		"""
		cursor.execute(sql)

		# create the item table if it doesn't exist
		sql = """
		CREATE TABLE IF NOT EXISTS `item` ( `item_record_id` INTEGER, `item_record_num` INTEGER, `bib_record_id` INTEGER, `bib_record_num` INTEGER, `creation_date` TEXT, `record_last_updated` TEXT, `barcode` TEXT, `agency_code_num` INTEGER, `location_code` TEXT, `checkout_statistic_group_code_num` INTEGER, `checkin_statistics_group_code_num` INTEGER, `checkout_date` TEXT, `due_date` TEXT, `patron_branch_code` TEXT, `last_checkout_date` TEXT, `last_checkin_date` TEXT, `checkout_total` INTEGER, `renewal_total` INTEGER, `isbn` TEXT, `item_format` TEXT, `item_status_code` TEXT, `price` TEXT, `item_callnumber` TEXT, `is_deleted` INTEGER DEFAULT 0, PRIMARY KEY(`item_record_id`) )
		"""
		cursor.execute(sql)
		
		self.sqlite_conn.commit()		
		cursor.close()
		cursor = None


	def create_remote_temp_tables(self):
		# open the sqlfile
		sql_string_bib_data = open('temp_table-bib_data.sql', mode='r', encoding='utf-8-sig').read()
		sql_string_item_data = open('temp_table-item_data.sql', mode='r', encoding='utf-8-sig').read()
		sql_string_hold_data = open('temp_table-hold_data.sql', mode='r', encoding='utf-8-sig').read()

		with self.pgsql_conn as conn:
			with conn.cursor() as cursor:
				# bib
				print('creating temp bib data table ...')
				cursor.execute(sql_string_bib_data)
				# item
				print('creating temp item data table ...')
				cursor.execute(sql_string_item_data)
				# hold
				print('creating temp hold data table ...')
				cursor.execute(sql_string_hold_data)
				print('done creating temp data tables.')

		cursor = None
		conn = None


	def rand_int(self, length):
		#~ simple random number generator for our named cursor
		return randint(10**(length-1), (10**length)-1)


	def gen_sierra_data(self, query):
		#~ fetch and yield self.itersize number of rows per round
		generator_cursor = "gen_cur" + str(self.rand_int(10))

		try:
			cursor = self.pgsql_conn.cursor(name=generator_cursor,
					cursor_factory=psycopg2.extras.NamedTupleCursor)
			cursor.itersize = self.itersize # sets the itersize
			cursor.execute(query)
			# cursor.execute('SELECT * FROM temp_stat_groups;')

			rows = None
			while True:
				rows = cursor.fetchmany(self.itersize)
				if not rows:
					break

				for row in rows:
					# debug
					# pdb.set_trace()
					yield row

			cursor.close()
			cursor = None

		except psycopg2.Error as e:
			print("psycopg2 Error: {}".format(e))


	def fill_local_db(self):
		# create the cursor
		cursor = self.sqlite_conn.cursor()

		# insert the bib data
		bib_csv_file = open(self.csv_bib_file_name, 'w')
		bib_csv_writer = csv.writer(bib_csv_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
		# quoting=csv.QUOTE_MINIMAL

		sql_bib_insert = """
		INSERT OR REPLACE INTO bib (
			bib_record_num, --1
			bib_record_id, --2
			control_numbers, --3
			creation_date, --4
			record_last_updated, --5
			isbn, --6
			best_author, --7
			best_author_norm, --8
			best_title, --9
			best_title_norm, --10
			publisher, --11
			publish_year, --12
			bib_level_callnumber, --13
			indexed_subjects --14
		)

		VALUES
		(
			?, --1
			?, --2
			?, --3
			?, --4
			?, --5
			?, --6
			?, --7
			?, --8
			?, --9
			?, --10
			?, --11
			?, --12
			?, --13
			? --14
		);
		"""

		print('start bib export')
		row_counter = 0
		for row in self.gen_sierra_data(query='SELECT * FROM temp_bib_export'):
			row_counter += 1
			values = (
				row.bib_record_num,
				row.bib_record_id,
				row.control_numbers,
				row.creation_date,
				row.record_last_updated,
				row.isbn,
				row.best_author,
				row.best_author_norm,
				row.best_title,
				row.best_title_norm,
				row.publisher,
				row.publish_year,
				row.bib_level_callnumber,
				row.indexed_subjects
			)
			# do the insert
			cursor.execute(sql_bib_insert, values)
			# debug
			# pdb.set_trace()
				
			# write to csv file
			if(row_counter==1):
				# Write to the header
				# if we want to output all data to the .csv, the following may be useful
				# keys = row._asdict().keys()
				# print('row keys: {}'.format(keys))
				# MAKE SURE THESE MATCH THE OUTPUT ROWS
				bib_csv_writer.writerow(
					(
						'bib_record_num', 
						'creation_date',
						'record_last_updated',
						'isbn',
						'best_author',
						'best_title',
						'publisher',
						'publish_year',
						'bib_level_callnumber',
						'indexed_subjects'
					)
				)

			bib_csv_writer.writerow(
				(
					row.bib_record_num, 
					row.creation_date,
					row.record_last_updated,
					row.isbn,
					row.best_author,
					row.best_title,
					row.publisher,
					row.publish_year,
					row.bib_level_callnumber,
					row.indexed_subjects
				)
			)

			# commit values to the local database every self.itersize times through
			if(row_counter % self.itersize == 0):
				self.sqlite_conn.commit()
				print('.',end='')
				# self.sqlite_conn.commit()
				# debug
				# pdb.set_trace()
				# print(row)
		self.sqlite_conn.commit()
		bib_csv_file.close()
		print("\ndone with bib export")
		# /insert the bib data

		###

		# insert the item data
		item_csv_file = open(self.csv_item_file_name, 'w')
		item_csv_writer = csv.writer(item_csv_file, delimiter='|', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

		sql_item_insert = """
		INSERT OR REPLACE INTO item (
			item_record_id, --1
			item_record_num, --2
			bib_record_id, --3
			bib_record_num, --4
			creation_date, --5
			record_last_updated, --6
			barcode, --7
			agency_code_num, --8
			location_code, --9
			checkout_statistic_group_code_num, --10
			checkin_statistics_group_code_num, --11
			checkout_date, --12
			due_date, --13
			patron_branch_code, --14
			last_checkout_date, --15
			last_checkin_date, --16
			checkout_total, --17
			renewal_total, --18
			isbn, --19
			item_format, --20
			item_status_code, --21
			price, --22
			item_callnumber --23
		)

		VALUES
		(
			?, --1
			?, --2
			?, --3
			?, --4
			?, --5
			?, --6
			?, --7
			?, --8
			?, --9
			?, --10
			?, --11
			?, --12
			?, --13
			?, --14
			?, --15
			?, --16
			?, --17
			?, --18
			?, --19
			?, --20
			?, --21
			?, --22
			? --23
		);
		"""

		row_counter = 0
		# Write to the header
		# if we want to output all data to the .csv, the following may be useful
		# keys = row._asdict().keys()
		# print('row keys: {}'.format(keys))
		# MAKE SURE THESE MATCH THE OUTPUT ROWS
		item_csv_writer.writerow(
			(
				'item_record_num',
				'bib_record_num',
				'creation_date',
				'record_last_updated',
				'barcode',
				'agency_code_num',
				'location_code',
				'checkout_statistic_group_code_num',
				'checkin_statistics_group_code_num',
				'checkout_date',
				'due_date',
				'patron_branch_code',
				'last_checkout_date',
				'last_checkin_date',
				'checkout_total',
				'renewal_total',
				'isbn',
				'item_format',
				'item_status_code',
				'price',
				'item_callnumber'
			)
		)

		print('start item export')
		for row in self.gen_sierra_data(query='SELECT * FROM temp_item_export'):
			row_counter += 1

			item_csv_writer.writerow(
				(
					row.item_record_num,
					row.bib_record_num,
					row.creation_date,
					row.record_last_updated,
					row.barcode,
					row.agency_code_num,
					row.location_code,
					row.checkout_statistic_group_code_num,
					row.checkin_statistics_group_code_num,
					row.checkout_date,
					row.due_date,
					row.patron_branch_code,
					row.last_checkout_date,
					row.last_checkin_date,
					row.checkout_total,
					row.renewal_total,
					row.isbn,
					row.item_format,
					row.item_status_code,
					row.price,
					row.item_callnumber
				)
			)

			values = (
				row.item_record_id,
				row.item_record_num,
				row.bib_record_id,
				row.bib_record_num,
				row.creation_date,
				row.record_last_updated,
				row.barcode,
				row.agency_code_num,
				row.location_code,
				row.checkout_statistic_group_code_num,
				row.checkin_statistics_group_code_num,
				row.checkout_date,
				row.due_date,
				row.patron_branch_code,
				row.last_checkout_date,
				row.last_checkin_date,
				row.checkout_total,
				row.renewal_total,
				row.isbn,
				row.item_format,
				row.item_status_code,
				row.price,
				row.item_callnumber
			)
			# do the insert
			cursor.execute(sql_item_insert, values)
			# debug
			# pdb.set_trace()

			# commit values to the local database every self.itersize times through
			if(row_counter % self.itersize == 0):
				self.sqlite_conn.commit()
				print('.', end='', flush=True)
				# self.sqlite_conn.commit()
				# debug
				# pdb.set_trace()
				# print(row)
		self.sqlite_conn.commit()
		item_csv_file.close()
		print("\ndone with item export")
		# /insert the item data

		#
		# insert the hold data
		hold_csv_file = open(self.csv_hold_file_name , 'w')
		hold_csv_writer = csv.writer(hold_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

		row_counter = 0
		# write to the header ...
		hold_csv_writer.writerow(
			(
				'bib_record_num',
				'holds'
			)
		)

		print('start hold export')
		for row in self.gen_sierra_data(query='SELECT bib_record_num, holds FROM temp_holds'):
			row_counter += 1
			hold_csv_writer.writerow(
				(
					row.bib_record_num,
					row.holds
				)
			)

			if(row_counter % self.itersize == 0):
				print('.',end='')

		hold_csv_file.close()
		print("\ndone with hold export")


#~ run the app!
start_time = datetime.now()
print('starting import at: \t\t{}'.format(start_time))
app = App()
end_time = datetime.now()
print('finished import at: \t\t{}'.format(end_time))
print('total import time: \t\t{}'.format(end_time - start_time))