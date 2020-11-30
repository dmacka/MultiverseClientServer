#!/bin/sh

# Make some checks to see if the current directory seems like
# source or destination media tree.  A source tree must have
# the media subdirectories.  A destination tree must either
# not exist, be empty, or contain the media subdirectories
validate_media_tree () {
	dir=$1
	desc=$2
	target_msg=$3
	# Only check for empty if it's a destination media tree
	if [ -n "${target_msg}" ]; then
		if [ ! -d ${dir} ] || [ -n $(ls ${dir}) ]; then
			return
		fi
	fi
	if [ ! -d "${dir}/Meshes" ] || [ ! -d "${dir}/Materials" ] || [ ! -d "${dir}/Textures" ] || [ ! -d "${dir}/Interface" ]; then
		echo "The directory '${dir}' doesn't seem to be a ${desc}${target_msg}; exiting"
		exit
	fi
}

# Check that . is a source media tree, then generate the assets 
# by calling asset packager, then create a .zip file from them
# with WinRAR, then copy the new zip files to a destination 
# directory
create_world_assets () {
	validate_media_tree "$(pwd)" "source media tree"
	kind=$1
	world_name=$2
	if [ -n "${3}" ]; then
		assets_file_name=$3
	else
		assets_file_name="${kind}Assets"
	fi
	echo "Creating ${kind}Assets for kind '${kind}', world_name '${world_name}'"
	new_media="${new_assets}/${kind}Assets"
    # Create the target directory, or clear its previous contents
	if [ -d $new_media ]; then
		validate_media_tree "${new_media}" "destination media tree" ", so refusing to rm -rf it"
		echo "Deleting previous contents of ${new_media}"
		rm -rf ${new_media}/*
	else
		mkdir $new_media
	fi
	if [ -n "${world_name}" ]; then
		cmd="${asset_packager} --new_asset_repository ${new_media} --assetlist_file WorldEditorAssets.assetlist --assetlist_file ${assets_file_name}.assetlist --world_name $world_name --worldassets_file ${server_config}/${world_name}/${world_name}.worldassets"
	else
		# Only used to generate WorldEditorAssets.zip
		cmd="${asset_packager} --new_asset_repository ${new_media} --assetlist_file ${kind}Assets.assetlist"
	fi
	echo "Invoking ${cmd}"
	$(${cmd})
	echo "Creating archive ${new_media}/${assets_file_name}.zip"
	WinRAR.exe a "${new_media}/${assets_file_name}" -afzip -r -ep1 "${new_media}/*.*"
	echo "Copying zip file to ${zip_directory}/${assets_file_name}.zip"
	cp "${new_media}/${assets_file_name}.zip" "${zip_directory}/${assets_file_name}.zip"
	echo "Done with ${assets_file_name}"
	echo
}

#########################################################################
#
# NOTE: You must be positioned in the media tree to run this shell script!!!
#
# Change the values of the variables below to conform to the 
# the layout of directories on your machine 
#
########################################################################

asset_packager=""
new_assets=""
server_config=""
zip_directory=""

# E.g., the values I use on my laptop are:
#asset_packager="C:/Multiverse/Client/Tools/AssetPackager/bin/Debug/AssetPackager.exe"
#new_assets="C:/Junk/Assets"
#server_config="C:/Multiverse/Server/multiverse/config"
#zip_directory="C:/Junk/1.0Assets"

create_world_assets WorldEditor

create_world_assets SampleWorld sampleworld SampleAssets

create_world_assets SocialWorld mv_social

create_world_assets FantasyWorld mv_fantasy
