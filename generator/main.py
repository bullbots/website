import os
import shutil
import markdown
from distutils.dir_util import copy_tree

BUILD_DIRECTORY = '..\\docs'

TITLE = 'TITLE'
NAVIGATION = 'NAVIGATION'
MAIN_CONTENT = 'MAIN CONTENT'
CUSTOM_SCRIPTS = "CUSTOM SCRIPTS"


def generate_navigation() -> str:
    nav = ''
    with open(os.path.join("..\\pages", "navigation.txt"), 'r') as file:
        while file:
            page = file.readline()
            if page == '':
                break
            nav += '<li><a href=\"%s.html\">%s</a></li>\n' % (page.strip(), page.replace('-', ' ').strip().title())

    print("Generated navigation:")
    print(nav)
    return nav


def generate_sponsors() -> str:
    sponsor_images = ""
    for filename in os.listdir("..\\assets\\home\\sponsors"):
        print(filename)
        sponsor_images += "<img class='sponsor-image' src='assets/home/sponsors/" + filename + \
                          "' onerror=\"this.style.display='none'\">\n"

    return sponsor_images


# Custom pages:
def robots_page(nav):
    print("Generating robot.html from /pages/robots/ directory")
    try:
        robot_generated_html = ""
        # Copy any custom js and css
        custom_scripts = ""
        try:
            shutil.copy2("..\\pages\\robots\\robots.js", BUILD_DIRECTORY)
            custom_scripts += "<script src=\"robots.js\" defer></script>\n"
        except FileNotFoundError:
            print("No file found for \"robots.js\"")
        try:
            shutil.copy2("..\\pages\\robots\\robots.css", BUILD_DIRECTORY)
            custom_scripts += "<link rel=\"stylesheet\" href=\"robots.css\">"
        except FileNotFoundError:
            print("No file found for \"robots.css\"")

        # Generate the content for each year
        for filename in reversed(os.listdir("..\\pages\\robots\\years")):
            robot_template_html = """
            <div class="robot-widget animated-hidden">
                <h2>SEASON - CHALLENGE TITLE</h2>
                <div>
                    <img src="assets/robots/IMAGE FILE NAME.png" onerror="this.style.display='none'">
                    <div>
                        <h3>ROBOT NAME</h3>
                        <p>DESCRIPTION</p>
                    </div>
                </div>
            </div>
            """
            with open(os.path.join("..\\pages\\robots\\years", filename), 'r') as file:
                print("Reading file " + filename)
                image_file_name = filename.split(".")[0]
                season = image_file_name.replace("-", " ").title()
                challenge_title = file.readline().strip()
                robot_name = file.readline().strip()
                description = file.read()
                robot_template_html = robot_template_html.replace("SEASON", season)
                robot_template_html = robot_template_html.replace("IMAGE FILE NAME", image_file_name)
                robot_template_html = robot_template_html.replace("CHALLENGE TITLE", challenge_title)
                robot_template_html = robot_template_html.replace("ROBOT NAME", robot_name)
                robot_template_html = robot_template_html.replace("DESCRIPTION", description)
                # Add each year's content to the whole
                robot_generated_html += robot_template_html

        # Fill in the template with all of the generated content
        template_html = open("..\\template\\template.html").read()
        template_html = template_html.replace(TITLE, "Robots")
        template_html = template_html.replace(NAVIGATION, nav)
        template_html = template_html.replace(MAIN_CONTENT, robot_generated_html)
        template_html = template_html.replace(CUSTOM_SCRIPTS, custom_scripts)

        generated_html = open(BUILD_DIRECTORY + "\\robots.html", 'x')
        generated_html.write(template_html)
    except FileNotFoundError:
        print("Attempt to generate \"Robots\" page was unsuccessful because the path ..\\pages\\robots\\years could "
              "not be found.")


def alumni_page(nav):
    print("Generating alumni.html from /pages/alumni/ directory")
    try:
        alumni_generated_html = ""
        # Copy any custom js and css
        custom_scripts = ""
        try:
            shutil.copy2("..\\pages\\alumni\\alumni.js", BUILD_DIRECTORY)
            custom_scripts += "<script src=\"alumni.js\" defer></script>\n"
        except FileNotFoundError:
            print("No file found for \"alumni.js\"")
        try:
            shutil.copy2("..\\pages\\alumni\\alumni.css", BUILD_DIRECTORY)
            custom_scripts += "<link rel=\"stylesheet\" href=\"alumni.css\">"
        except FileNotFoundError:
            print("No file found for \"alumni.css\"")

        # Generate the content for each year
        for filename in reversed(os.listdir("..\\pages\\alumni\\years")):
            alumni_template_html = """
<div class="alumni-widget animated-hidden">
    <h2>YEAR</h2>
    <div>
ALUMNI
    </div>
</div>
            """
            with open(os.path.join("..\\pages\\alumni\\years", filename), 'r') as file:
                print("Reading file " + filename)
                year = filename.split(".")[0].replace("-", " ").title()
                alumni = ""
                while file:
                    student = file.readline().strip()
                    if student == '':
                        break
                    alumni += "<p>%s</p>\n" % student
                alumni_template_html = alumni_template_html.replace("YEAR", year)
                alumni_template_html = alumni_template_html.replace("ALUMNI", alumni)
                # Add each year's content to the whole
                alumni_generated_html += alumni_template_html

        # Fill in the template with all of the generated content
        template_html = open("..\\template\\template.html").read()
        template_html = template_html.replace(TITLE, "Alumni")
        template_html = template_html.replace(NAVIGATION, nav)
        template_html = template_html.replace(MAIN_CONTENT, alumni_generated_html)
        template_html = template_html.replace(CUSTOM_SCRIPTS, custom_scripts)

        generated_html = open(BUILD_DIRECTORY + "\\alumni.html", 'x')
        generated_html.write(template_html)
    except FileNotFoundError:
        print("Attempt to generate \"Alumni\" page was unsuccessful because the path ..\\pages\\alumni\\years could "
              "not be found.")


if __name__ == "__main__":
    # Delete ..\docs\ directory to be rewritten
    folder = BUILD_DIRECTORY+'\\'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    navigation = generate_navigation()
    # navigation = ""
    # # Add Alumni and Robots to navigation manually
    # navigation += "<li><a href=\"alumni.html\">Alumni</a></li>\n"
    # navigation += "<li><a href=\"robots.html\">Robots</a></li>\n"
    # for (root, dirs, files) in os.walk('..\\pages', topdown=True):
    #     for file in [f for f in files if (f.endswith(".md") or f.endswith(".html")) and not 'index' in f]:
    #         filename = file.split(".")[0]
    #         navigation += "<li><a href=\"%s\">%s</a></li>\n" % (filename + ".html", filename.replace("-", " ").title())

    # Generate the custom pages
    robots_page(navigation)
    alumni_page(navigation)

    # Copy template and custom files
    shutil.copy2("..\\template\\template-script.js", BUILD_DIRECTORY)
    shutil.copy2("..\\template\\template-styles.css", BUILD_DIRECTORY)
    copy_tree("..\\assets", "..\\docs\\assets")
    for (root, dirs, files) in os.walk('..\\pages', topdown=True):
        for file in files:
            filename = file.split(".")[0]
            # Convert each markdown file into an html snippet and create a full file using the template html
            if file.endswith(".md"):
                print("Generating \"%s.html\" from \"%s.md\"" % (filename, filename))
                md = markdown.markdown(open(root + "\\" + file).read())

                template_html = open("..\\template\\template.html").read()
                if filename == "index":
                    template_html = template_html.replace(TITLE, "Bullbots")
                else:
                    template_html = template_html.replace(TITLE, filename.replace("-", " ").title())
                template_html = template_html.replace(NAVIGATION, navigation)
                template_html = template_html.replace(MAIN_CONTENT, md)
                template_html = template_html.replace(CUSTOM_SCRIPTS, "")

                # print("gen_path:", gen_path)
                # generated_html = open(gen_path + filename + ".html", 'x')
                generated_html = open("..\\docs\\" + filename + ".html", 'x')
                generated_html.write(template_html)
            elif file.endswith(".html"):
                print("Reading \"%s.html\"" % filename)

                # Copy any custom js and css
                custom_scripts = ""
                try:
                    shutil.copy2(root + "\\" + filename + ".js", BUILD_DIRECTORY)
                    custom_scripts += "<script src=\"%s.js\" defer></script>\n" % filename
                except FileNotFoundError:
                    print("No file found for \"%s.js\"" % file)
                try:
                    shutil.copy2(root + "\\" + filename + ".css", BUILD_DIRECTORY)
                    custom_scripts += "<link rel=\"stylesheet\" href=\"%s.css\">" % filename
                except FileNotFoundError:
                    print("No file found for \"%s.css\"" % file)

                custom_html = open(root + "\\" + file).read()

                template_html = open("..\\template\\template.html").read()
                if filename == "index":
                    template_html = template_html.replace(TITLE, "Bullbots")
                    custom_html = custom_html.replace("SPONSORS", generate_sponsors())
                else:
                    template_html = template_html.replace(TITLE, filename.replace("-", " ").title())
                template_html = template_html.replace(NAVIGATION, navigation)
                template_html = template_html.replace(MAIN_CONTENT, custom_html)
                template_html = template_html.replace(CUSTOM_SCRIPTS, custom_scripts)

                generated_html = open(BUILD_DIRECTORY + "\\" + filename + ".html", 'x')
                generated_html.write(template_html)
