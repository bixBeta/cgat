#!/bin/env python
import sys, re, os
import optparse

USAGE="""%s [OPTIONS]

set up a new CGAT pipeline in the current directory.
""" % sys.argv[0]

def main( argv = sys.argv ):

    parser = optparse.OptionParser( version = "%prog version: $Id$", usage = USAGE)

    parser.add_option("-d", "--dest", dest="destination", type="string",
                      help="destination directory." )

    parser.add_option("-n", "--name", dest="name", type="string",
                      help="name of this pipeline." )

    parser.add_option("-f", "--force", dest="force", action="store_true",
                      help="overwrite existing files." )
    
    parser.set_defaults(
        destination = ".",
        name = None,
        force = False,
        )
    
    (options, args) = parser.parse_args()

    if not options.name: raise ValueError( "please provide a pipeline name" )

    reportdir = os.path.abspath( "src/pipeline_docs/pipeline_%s" % options.name )

    dest = options.destination
    name = options.name

    # create directories
    for d in ("", "src", "report", "work",
              "src/pipeline_docs", 
              reportdir,
              "%s/_templates" % reportdir,
              "%s/pipeline" % reportdir,
              "%s/trackers" % reportdir ):

        dd = os.path.join( dest, d )
        if not os.path.exists( dd ): os.makedirs( dd )
        
    # copy files
    # replaces all instances of template with options.name within
    # filenames and inside files.
    rx_file = re.compile( "template" )
    rx_template = re.compile( "@template@" )
    rx_reportdir = re.compile( "@reportdir@" )

    srcdir = os.path.dirname( __file__ )

    def copy( src, dst ):
        fn_dest = os.path.join( dest, dst, rx_file.sub(name, src) )
                                    
        fn_src = os.path.join( srcdir, "pipeline_template", src)

        if os.path.exists( fn_dest ) and not options.force:
            raise OSError( "file %s already exists - not overwriting." % fn_dest )

        outfile = open(fn_dest, "w")
        infile = open(fn_src )
        for line in infile:
            outfile.write( rx_reportdir.sub( reportdir, 
                                             rx_template.sub( name, line ) ))
            
        outfile.close()
        infile.close()

    for f in ( "sphinxreport.ini",
               "conf.py" ):
        copy( f, "work" )
        
    for f in ( "pipeline_template.py",
               "pipeline_template.ini" ):
        copy( f, "src" )

    for f in ( "cgat_logo.png",
               "index.html",
               "gallery.html" ):
        copy( f, "%s/_templates" % reportdir )

    for f in ( "contents.rst",
               "pipeline.rst",
               "analysis.rst",
               "__init__.py" ):
        copy( f, reportdir )

    for f in ( "Dummy.rst",
               "Methods.rst"):
        copy( f, "%s/pipeline" % reportdir )

    for f in ( "TemplateReport.py", ):
        copy( f, "%s/trackers" % reportdir )

    absdest = os.path.abspath( dest )

    print """
Welcome to your new %(name)s CGAT pipeline.

All files have been successfully copied to `%(dest)s`. In order to start
the pipeline, go to `%(dest)s/work`

   cd %(dest)s/work

You can start the pipeline by typing:

   python ../src/pipeline_%(name)s.py -v 5 -p 5 make full

To build the report, type:

   python ../src/pipeline_%(name)s.py -v 5 -p 5 make build_report

The report will be in file:/%(absdest)s/work/report/html/index.html.


""" % locals()

   
if __name__ == "__main__":
    sys.exit(main())