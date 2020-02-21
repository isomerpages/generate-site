#!/usr/bin/env python2

import subprocess

def create_repo():
	try:
		repo_name = raw_input("Type the name of the website you are creating (replace whitespaces with hyphens), e.g. for isomerpages/new-repo, type new-repo \n")
		repo_full_name = "../" + repo_name
		command = "cp -r isomerpages-base " + repo_full_name
		subprocess.call(command, shell=True)
		print repo_full_name + " directory created"

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
				command = 'echo "---\ntitle: ' + to_human_readable_string(simple_page) + '\npermalink: /' + simple_page + '/\n---" >> ' + simple_path_path
				subprocess.call(command, shell=True)
				print "		Created file: " + simple_path_path

				# Add simple pages to navigation yml
				command = 'echo "  - title: ' + to_human_readable_string(simple_page) + '\n    url: /' + simple_page + '/" >> ' + nav_yml_path
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

				command = 'echo "  - title: ' + to_human_readable_string(leftnav_page_title) + '\n    collection: ' + leftnav_page_title + '" >> ' + nav_yml_path
				subprocess.call(command, shell=True)
				print "		Added " + leftnav_page_title + " collection to navigation.yml"

				# Create leftnav pages in folder
				for index, name in enumerate(leftnav_page_names.split(',')):					
					leftnav_page_path = leftnav_folder_path + '/' + str(index) + '-' + name + '.md'
					command = 'echo "---\ntitle: ' + to_human_readable_string(name) + '\npermalink: /' + leftnav_page_title + '/' + name + '/\n---" >> ' + leftnav_page_path
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

			homepage_path = repo_full_name + '/index.md'
			command = 'echo "    - resources:\n        title: Media\n        subtitle: Learn more\n        button: View More" >> ' + homepage_path
			subprocess.call(command, shell=True)
			print "Updated homepage file: " + homepage_path

			# Create resource folder
			resource_folder_path = repo_full_name + '/' + resource_title
			resource_index_path = resource_folder_path + '/index.html'
			command = 'mkdir ' + resource_folder_path
			subprocess.call(command, shell=True)
			print "Created resources folder: " + resource_folder_path

			# Create index file in resource folder
			command = 'echo "---\nlayout: resources\ntitle: '+ to_human_readable_string(resource_title) + '\n---" >> ' + resource_index_path
			subprocess.call(command, shell=True)
			print "Created resources index html: " + resource_index_path

			# Add resources to navigation yml
			command = 'echo "  - title: ' + to_human_readable_string(resource_title) + '\n    resource_room: true" >> ' + nav_yml_path
			subprocess.call(command, shell=True)
			print "		Added resources to navigation.yml"

			# Add resource name to config yml
			command = 'echo "resources_name: ' + resource_title + '" >> ' + config_yml_path
			subprocess.call(command, shell=True)

			for name in resource_subcategory_names.split(','):
				resource_subcategory_folder_path = resource_folder_path + '/' + name
				resource_subcategory_index_path = resource_subcategory_folder_path + '/index.html'
				resource_subcategory_posts_folder_path = resource_subcategory_folder_path + '/_posts'
				resource_subcategory_post_path = resource_subcategory_posts_folder_path + '/2019-01-01-test.md'

				# Create subcategory folder
				command = 'mkdir ' + resource_subcategory_folder_path
				subprocess.call(command, shell=True)
				print "		Created resources subcategory folder: " + resource_subcategory_folder_path

				# Create index file in subcategory folder
				command = 'echo "---\nlayout: resources-alt\ntitle: ' + to_human_readable_string(resource_title) + '\n---" >> ' + resource_subcategory_index_path
				subprocess.call(command, shell=True)
				print "			Created index file in resources subcategory folder: " + resource_subcategory_index_path

				# Create subcategory posts folder
				command = 'mkdir ' + resource_subcategory_posts_folder_path
				subprocess.call(command, shell=True)
				print "			Created resources subcategory posts folder: " + resource_subcategory_posts_folder_path

				# Create post in subcategory posts folder
				command = 'echo "---\nlayout: post\ntitle:  \"Sample post for ' + to_human_readable_string(name) + '\"\npermalink: \"/' + resource_title + '/' + name + '/test\"\n---\nLorem ipsum sit amet" >> ' + resource_subcategory_post_path 
				subprocess.call(command, shell=True)
				print "			Created post in resources subcategory posts folder: " + resource_subcategory_post_path

	except:
		print "Failed to create resource room"
		exit(0)

def configuration_cleanup(repo_full_name, config_yml_path):
	# Populate the remainder of the configuration for index.md and config.yml
	try:
		homepage_path = repo_full_name + '/index.md'
		command = 'echo "---" >> ' + homepage_path
		subprocess.call(command, shell=True)
		print "Completed homepage file: " + homepage_path

		command = 'echo "\n##################################################################################################################\n# Everything below this line is Isomer-specific configuration. There should not be a need to edit these settings #\n##################################################################################################################\npermalink: none\nbaseurl: \\"\\"\nexclude: [travis-script.js, .travis.yml, README.md, package.json, package-lock.json, node_modules, vendor/bundle/, vendor/cache/, vendor/gems/, vendor/ruby/, Gemfile, Gemfile.lock]\ninclude: [_redirects]\ndefaults:\n  - scope:\n      path: \\"\\"\n    values:\n      layout: \\"page\\"\n# Custom CSS file path\ncustom_css_path: \\"/misc/custom.css\\"\ncustom_print_css_path: \\"/assets/css/print.css\\"\npaginate: 12\nremote_theme: isomerpages/isomerpages-template@next-gen\nsafe: false\nplugins:\n  - jekyll-feed\n  - jekyll-assets\n  - jekyll-paginate\n  - jekyll-sitemap\ndescription: test test\n" >> ' + config_yml_path
		subprocess.call(command, shell=True)
		print "Completed config.yml"
	except:
		print "Configuration cleanup failed"
		exit(0)

def run_npm(repo_full_name):
	try:
		subprocess.check_call("npm init -y", cwd=repo_full_name, shell=True)

		# Travis scripts are no longer used in repos
		# subprocess.check_call("npm install @isomerpages/isomerpages-travisci-scripts", cwd=repo_full_name, shell=True)
		# print "Isomer TravisCI scripts successfully installed! Remember to configure SLACK_URI on TravisCI and uncomment the code in travis-script.js for production."
	except:
		print "Failed to initialize npm package and/or install TravisCI script package from npm"
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
	configuration_cleanup(repo_full_name, config_yml_path)
	run_npm(repo_full_name)

if __name__ == "__main__":
    main()
