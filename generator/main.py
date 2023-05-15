import os
import shutil
import markdown
from distutils.dir_util import copy_tree

BUILD_DIRECTORY = '..\\docs'

TITLE = 'TITLE'
NAVIGATION = 'NAVIGATION'
MAIN_CONTENT = 'MAIN CONTENT'
CUSTOM_SCRIPTS = "CUSTOM SCRIPTS"


# Custom pages:
def robots_page(nav):
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
                    <img src="assets/robots/SEASON.png">
                    <div>
                        <h3>ROBOT NAME</h3>
                        <p>DESCRIPTION</p>
                    </div>
                </div>
            </div>
            """
            with open(os.path.join("..\\pages\\robots\\years", filename), 'r') as file:
                print("Reading file " + filename)
                season = filename.split(".")[0]
                challenge_title = file.readline(-1)
                robot_name = file.readline(-1)
                description = file.read()
                robot_template_html = robot_template_html.replace("SEASON", season)
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

    navigation = ""
    for (root, dirs, files) in os.walk('..\\pages', topdown=True):
        for file in [f for f in files if (f.endswith(".md") or f.endswith(".html")) and not f == 'index.md']:
            filename = file.split(".")[0]
            navigation += "<li><a href=\"%s\">%s</a></li>\n" % (filename + ".html", filename.replace("-", " ").title())

    # Add Robots to navigation
    navigation += "<li> <a href=robots.html>Robots</a></li>\n"

    print("Generated navigation:")
    print(navigation)

    # Generate the custom pages
    robots_page(navigation)

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
                    print("No file found for \"%s\"" % file)
                try:
                    shutil.copy2(root + "\\" + filename + ".css", BUILD_DIRECTORY)
                    custom_scripts += "<link rel=\"stylesheet\" href=\"%s.css\">" % filename
                except FileNotFoundError:
                    print("No file found for \"%s\"" % file)

                custom_html = open(root + "\\" + file).read()

                template_html = open("..\\template\\template.html").read()
                template_html = template_html.replace(TITLE, filename.replace("-", " ").title())
                template_html = template_html.replace(NAVIGATION, navigation)
                template_html = template_html.replace(MAIN_CONTENT, custom_html)
                template_html = template_html.replace(CUSTOM_SCRIPTS, custom_scripts)

                generated_html = open(BUILD_DIRECTORY + "\\" + filename + ".html", 'x')
                generated_html.write(template_html)
