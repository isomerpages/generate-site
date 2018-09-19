import subprocess

def create_repo():
	try:
		repo_name = raw_input("Type the name of the website you are creating (replace whitespaces with hyphens), e.g. for isomerpages/new-repo, type new-repo \n")
		repo_full_name = "../isomerpages-" + repo_name
		command = "cp -r isomerpages-base " + repo_full_name
		subprocess.call(command, shell=True)
		print repo_full_name + " directory created"

		# Add baseurl into config yml
		config_yml_path = repo_full_name + '/_config.yml'
		command = 'echo "baseurl: /isomerpages-' + repo_name + '" >> ' + config_yml_path
		subprocess.call(command, shell=True)

		return repo_full_name

	except:
		print "Failed to create new repo"
		exit(0)

def create_simple_pages(repo_full_name, nav_yml_path):
	try:
		user_input = raw_input("Type your list of simple-pages that you want to create with spaces, e.g. faq privacy-statement terms-of-use who-we-are \nIf there are no simple pages, please hit enter\n")
		if (user_input != ''):
			simple_pages_list = user_input.split()

			# Create simple page
			for simple_page in simple_pages_list:
				simple_path_path = repo_full_name + '/pages/' + simple_page + '.md'
				command = 'echo "---\nlayout: simple-page\ntitle: ' + to_human_readable_string(simple_page) + '\npermalink: /' + simple_page + '/\nbreadcrumb: ' + to_human_readable_string(simple_page) + '\n---" >> ' + simple_path_path
				subprocess.call(command, shell=True)
				print "		Created file: " + simple_path_path

				# Add simple pages to navigation yml
				command = 'echo "- title: ' + to_human_readable_string(simple_page) + '\n  url: /' + simple_page + '/" >> ' + nav_yml_path
				subprocess.call(command, shell=True)
				print "		Added simple page to navigation.yml"

	except:
		print "Failed to create simple pages"
		exit(0)

def create_leftnav_pages(repo_full_name, nav_yml_path, config_yml_path):
	try:
		user_input = raw_input("Type your list of leftnav-pages titles and their subpages in the sequence you would like them to be displayed, e.g. left-nav-one:sub-page-A,sub-page-B left-nav-two:sub-page-C,sub-page-D\nIf there are no leftnav pages, please hit enter\n")
		if (user_input != ''):
			# Add leftnav pages into config yml
			command = 'echo "collections:" >> ' + config_yml_path
			subprocess.call(command, shell=True)

			array = user_input.split()
			for leftnav_page_config in array:
				config_array = leftnav_page_config.split(':')
				leftnav_page_title = config_array[0]
				leftnav_page_names = config_array[1]

				# Create leftnav page folder
				leftnav_folder_path = repo_full_name + '/_' + leftnav_page_title
				command = 'mkdir ' + leftnav_folder_path
				subprocess.call(command, shell=True)
				print "Created folder: " + leftnav_folder_path

				command = 'echo "  ' + leftnav_page_title + ':\n    output: true" >> ' + config_yml_path
				subprocess.call(command, shell=True)

				# Create leftnav pages in folder
				for index, name in enumerate(leftnav_page_names.split(',')):
					# Add leftnav pages to navigation yml
					if index == 0:
						command = 'echo "- title: ' + to_human_readable_string(leftnav_page_title) + '\n  url: /' + leftnav_page_title + '/' + name + '/\n  sub-links:\n  - title: ' + to_human_readable_string(name) + '\n    url: /' + leftnav_page_title + '/' + name + '/" >> ' + nav_yml_path
					else:
						command = 'echo "  - title: ' + to_human_readable_string(name) + '\n    url: /' + leftnav_page_title + '/' + name + '/" >> ' + nav_yml_path
					subprocess.call(command, shell=True)
					print "		Added leftnav page to navigation.yml"

					leftnav_page_path = leftnav_folder_path + '/' + name + '.md'
					command = 'echo "---\nlayout: leftnav-page-content\ntitle: ' + to_human_readable_string(name) + '\npermalink: /' + leftnav_page_title + '/' + name + '/\nbreadcrumb: ' + to_human_readable_string(name) + '\ncollection_name: ' + leftnav_page_title + '\n---" >> ' + leftnav_page_path
					subprocess.call(command, shell=True)
					print "		Created file: " + leftnav_page_path

	except:
		print "Failed to create leftnav pages"
		exit(0)

def create_resource_room(repo_full_name, nav_yml_path, config_yml_path):
	try:
		user_input = raw_input("Type the name of your resource room and their subcategories as such, e.g. resource-room:subcategory-A,subcategory-B,subcategory-C\nIf there is no resource room, please hit enter\n")
		if (user_input != ''):
			config_array = user_input.split(':')
			resource_title = config_array[0]
			resource_subcategory_names = config_array[1]

			homepage_yml_path = repo_full_name + '/_data/homepage.yml'
			command = 'echo "resources-title: Resources\nresources-subtitle: Be in the know\nresources-more-button: More Resources\nresources-more-button-url: ' + resource_title + '/" >> ' + homepage_yml_path
			subprocess.call(command, shell=True)
			print "Updated homepage yml file: " + homepage_yml_path

			# Create resource folder
			resource_folder_path = repo_full_name + '/' + resource_title
			resource_index_path = resource_folder_path + '/index.html'
			command = 'mkdir ' + resource_folder_path
			subprocess.call(command, shell=True)
			print "Created resources folder: " + resource_folder_path

			# Create index file in resource folder
			command = 'echo "---\nlayout: resources\ntitle: '+ to_human_readable_string(resource_title) + '\nfile_url: /'+ resource_title + '/\nbreadcrumb: '+ to_human_readable_string(resource_title) + '\n---" >> ' + resource_index_path
			subprocess.call(command, shell=True)
			print "Created resources index html: " + resource_index_path

			# Add resources to navigation yml
			command = 'echo "- title: ' + to_human_readable_string(resource_title) + '\n  url: /' + resource_title + '/\n  sub-links:\n  - title: All\n    url: /' + resource_title + '/" >> ' + nav_yml_path
			subprocess.call(command, shell=True)
			print "		Added resources to navigation.yml"

			# Add resource name to config yml
			command = 'echo "resources_name: ' + resource_title + '" >> ' + config_yml_path
			subprocess.call(command, shell=True)

			for name in resource_subcategory_names.split(','):
				resource_subcategory_folder_path = resource_folder_path + '/' + name
				resource_subcategory_index_path = resource_subcategory_folder_path + '/index.html'
				resource_subcategory_posts_folder_path = resource_subcategory_folder_path + '/_posts'
				resource_subcategory_post_path = resource_subcategory_posts_folder_path + '/2018-01-01-test.md'

				# Create subcategory folder
				command = 'mkdir ' + resource_subcategory_folder_path
				subprocess.call(command, shell=True)
				print "		Created resources subcategory folder: " + resource_subcategory_folder_path

				# Create index file in subcategory folder
				command = 'echo "---\nlayout: resources-alt\ntitle: ' + to_human_readable_string(resource_title) + '\npermalink: /'+ resource_title + '/'+ name + '/\nbreadcrumb: '+ to_human_readable_string(name) + '\n---" >> ' + resource_subcategory_index_path
				subprocess.call(command, shell=True)
				print "			Created index file in resources subcategory folder: " + resource_subcategory_index_path

				# Create subcategory posts folder
				command = 'mkdir ' + resource_subcategory_posts_folder_path
				subprocess.call(command, shell=True)
				print "			Created resources subcategory posts folder: " + resource_subcategory_posts_folder_path

				# Create post in subcategory posts folder
				command = 'echo "---\nlayout: post\ntitle:  \"Sample post for ' + to_human_readable_string(name) + '\"\ndate:   2018-01-01\npermalink: \"/' + resource_title + '/' + name + '/test\"\n---" >> ' + resource_subcategory_post_path 
				subprocess.call(command, shell=True)
				print "			Created post in resources subcategory posts folder: " + resource_subcategory_post_path

				# Add resource subcategory to navigation yml
				command = 'echo "  - title: ' + to_human_readable_string(name) + '\n    url: /' + resource_title + '/' + name + '/" >> ' + nav_yml_path
				subprocess.call(command, shell=True)
				print "		Added resources subcategory to navigation.yml"

	except:
		print "Failed to create resource room"
		exit(0)


def to_human_readable_string(string):
	new_str = ''
	should_be_upper = True
	for char in string:
		if should_be_upper == True:
			new_str += char.upper()
			should_be_upper = False
		elif char == '-':
			new_str += ' '
			should_be_upper = True
		else:
			new_str += char
	return new_str

def main():
	repo_full_name = create_repo()
	nav_yml_path = repo_full_name + '/_data/navigation.yml'
	config_yml_path = repo_full_name + '/_config.yml'
	create_simple_pages(repo_full_name, nav_yml_path)
	create_leftnav_pages(repo_full_name, nav_yml_path, config_yml_path)
	create_resource_room(repo_full_name, nav_yml_path, config_yml_path)

if __name__ == "__main__":
    main()
