#!/usr/bin/osascript
--
-- Download NAQT "You Gotta Know" Articles
--
-- This script automatically downloads all "You Gotta Know" articles from NAQT's website
-- and saves them as HTML files in the project's data/ygk directory.
--
-- WHY APPLESCRIPT?
--   The NAQT website is protected by Cloudflare, which blocks automated scraping tools
--   and headless browsers. By using AppleScript to control Safari, we can download the
--   articles as a regular browser session, which bypasses Cloudflare's bot detection.
--
-- USAGE:
--   Run from the project root directory:
--     ./bin/download-ygk-articles.scpt
--
-- REQUIREMENTS:
--   - macOS with Safari installed
--   - Safari must allow JavaScript from Apple Events (System Settings > Privacy & Security > Automation)
--   - Active internet connection
--   - Run from the anki-qb project root directory
--
-- WHAT IT DOES:
--   1. Opens Safari and navigates to the NAQT "You Gotta Know" index page
--   2. Extracts all article links from the page
--   3. Visits each article in a new tab
--   4. Saves the HTML content to data/ygk/
--   5. Closes the tab and moves to the next article
--
-- OUTPUT:
--   HTML files saved to: data/ygk/https___www_naqt_com_you_gotta_know_*.html
--
-- NOTE:
--   This process takes several minutes as it waits for each page to load.
--   You can monitor progress in Safari as it works through the articles.
--

-- Get the current working directory (project root)
set projectRoot to do shell script "pwd"

-- Set the directory to save files (data/ygk within project)
set saveDir to projectRoot & "/data/ygk/"

-- Create the directory if it doesn't exist
do shell script "mkdir -p " & quoted form of saveDir

tell application "Safari"
	activate
	open location "https://www.naqt.com/you-gotta-know/"

	-- Wait for the page to load
	delay 5

	-- Get all desired links
	set linkList to do JavaScript "
        Array.from(document.querySelectorAll('ul > li > span > a')).map(a => a.href).join('\\n');
    " in document 1

	set linkArray to paragraphs of linkList

	repeat with i from 1 to count of linkArray
		set thisLink to item i of linkArray
		if thisLink is not "" then
			-- Open the link in a new tab
			tell window 1
				set newTab to make new tab with properties {URL:thisLink}
				set current tab to newTab
			end tell
			delay 5 -- wait for page to load

			-- Get the HTML content
			set pageHTML to do JavaScript "document.documentElement.outerHTML;" in newTab

			-- Create a filename-safe version of the URL
			set safeName to do shell script "echo " & quoted form of thisLink & " | sed 's/[^a-zA-Z0-9]/_/g'"

			-- Write HTML to file
			do shell script "echo " & quoted form of pageHTML & " > " & quoted form of (POSIX path of saveDir & safeName & ".html")

			-- Close the tab after saving
			tell window 1 to close newTab
		end if
	end repeat
end tell
