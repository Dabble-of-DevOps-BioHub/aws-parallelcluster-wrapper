#!/usr/bin/env bash

### EasyBuild Installation and Module Deployment

##################################################################
### Deploy modules - Environmental Variables
##################################################################
sourcce /usr/share/lmod/lmod/init/bash
export ANACONDA3_BASE="$HOME/.local/anaconda3"
export EB_ENV=eb--4
export PATH=${ANACONDA3_BASE}/bin:$PATH
export EASYBUILD_PREFIX=/apps/easybuild/1.0
export ROBOT=/app/software-configs
export MODULEPATH=/apps/easybuild/1.0/modules/all:${MODULEPATH}

function install_miniconda {
#	curl -s -L https://repo.continuum.io/miniconda/Miniconda3-4.5.12-Linux-x86_64.sh > miniconda.sh
	curl -s -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > miniconda.sh

	chmod 777 miniconda.sh ; bash miniconda.sh -f -b -p $ANACONDA3_BASE
	rm miniconda.sh && \
	    export PATH=${ANACONDA3_BASE}/bin:$PATH && \
	    conda config --set show_channel_urls True && \
	    conda config --add channels conda-forge && \
	    conda config --add channels bioconda && \
	    conda config --set always_yes True && \
	    conda update --all --yes && \
	    conda config --set allow_softlinks False && \
	    conda clean -tipy
}


function install_easybuild {
	##################################################################
	## Add Easybuild Config
	## This is just a placeholder, but needed for some setups
	##################################################################
	mkdir -p $HOME/.config/easybuild

	##################################################################
	## Install Easybuild
	## Create a conda env with easybuild and nothing else
	##################################################################
	conda create -n ${EB_ENV} pip
	source activate ${EB_ENV} && pip install easybuild==4.3.2

	#################################################################
	## Install an Easybuild Config
	## Anaconda2 is a Core EB config
	## --software-name is a way of telling EB to look for software
	## from the repos instead of supplying a .eb file
	##################################################################
	# This times out if it's done from the initialization script
	# Just run it manually
	#source activate $EB_ENV && \
	#	eb --software-name Anaconda3
}

##################################################################
## Anaconda Setup
## We are using miniconda3/python3 from anaconda
## Be sure to change this if you are running as a your own user
##################################################################
install_miniconda
install_easybuild


# These are only here for documentation purposes
##################################################################
## Add Easybuild Configs
## These are custom configs outside of the Easybuild Main
##################################################################
#mkdir -p $HOME/.eb/custom_repos
#cd $HOME/.eb/custom_repos
#git clone my-custom-configs 
#cd $HOME

###################################################################
### Add Custom Easybuild Configs to the Robot Path
### Robot will tell EB to automatically pull in deps
### Robot-path will tell EB where to look for configs
###################################################################
#export ROBOT=$HOME/.eb/custom_repos/my-custom-configs

### Remove the --dry-run in order to actually install the module
#source activate $EB_ENV
#eb --dry-run  --robot --robot-paths=$ROBOT   software-version.eb
#
#### Using --extended-dry-run will give you more information
#eb --extended-dry-run  --robot --robot-paths=$ROBOT  software-version.eb
#
#module avail

###################################################################
