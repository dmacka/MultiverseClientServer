import re
import sha
import tarfile
import os.path
import shutil

class AssetTree:
    def __init__(self, clientDir, dstPath):
        # client dir is essentially the source directory
        self.client_dir = clientDir
        self.dst_path = dstPath
        self.dir_tree = {}
        self.manifest_entries = []
        self.ignores = []
        self.ignore_patterns = []
        self.excludes = []
        self.exclude_patterns = []
        self.dir_pattern = re.compile(r'/')

    def make_tar_file(self, tarfile_path):
        tar_file = tarfile.open(tarfile_path, "w")
        self.write_to_tar(tar_file)
        tar_file.close()
        
    def write_to_tar(self, kinds, tar_file):
        # add directories as versions of the MultiverseClient directory
        # this means that the permissions will be based on that
        tar_file.add(self.client_dir, self.dst_path, False)
        for entry in self.manifest_entries:
            if entry.kind in kinds:
                tar_file.add(self.client_dir + entry.src_path, entry.dst_path, False)
        for subdir_name in self.dir_tree.keys():
            self.dir_tree[subdir_name].write_to_tar(kinds, tar_file)
            
    def copy_media_files(self, kinds, prefix):
        # add directories as versions of the MultiverseClient directory
        # this means that the permissions will be based on that
        if not os.path.isdir(prefix + self.dst_path):
            os.mkdir(prefix + self.dst_path)
        for entry in self.manifest_entries:
            if entry.kind in kinds:
                shutil.copyfile(self.client_dir + entry.src_path, prefix + entry.dst_path)
        for subdir_name in self.dir_tree.keys():
            self.dir_tree[subdir_name].copy_media_files(kinds, prefix)
            
    # this should only be called on the root asset tree
    def add_asset_path(self, kind, src_path, dst_path = ""):
        if dst_path == "":
            dst_path = src_path
        # build a tree structure that will match our directory structure
        path_parts = self.dir_pattern.split(dst_path)
        self.add_asset(kind, path_parts, src_path, dst_path)

    def add_ignore(self, pattern):
        # build a tree structure that will match our directory structure
        self.ignores.append(pattern)
        self.ignore_patterns.append(re.compile(pattern))


    def add_exclude(self, pattern):
        # build a tree structure that will match our directory structure
        self.excludes.append(pattern)
        self.exclude_patterns.append(re.compile(pattern))

    def add_asset(self, kind, pathParts, src_path, dst_path):
        if len(pathParts) == 1:
            if os.path.isdir(self.client_dir + src_path):
                if not self.dir_tree.has_key(pathParts[0]):
                    self.dir_tree[pathParts[0]] = AssetTree(self.client_dir, self.dst_path + pathParts[0] + "/")
            elif os.path.isfile(self.client_dir + src_path):
                entry = ManifestEntry(kind, src_path, dst_path, pathParts[0])
                entry.compute_digest(self.client_dir)
                self.manifest_entries.append(entry)
            else:
                print "Invalid asset entry: " + self.client_dir + src_path
        elif len(pathParts) > 1:
            if not self.dir_tree.has_key(pathParts[0]):
                self.dir_tree[pathParts[0]] = AssetTree(self.client_dir, self.dst_path + pathParts[0] + "/")
            self.dir_tree[pathParts[0]].add_asset(kind, pathParts[1:], src_path, dst_path)

    def print_all_entries(self, f, rev, url):
        f.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        f.write("<patch_data revision=\"%s\" url=\"%s\">\n" % (rev, url))
        for entry in self.excludes:
            f.write("  <exclude pattern=\"%s\"/>\n" % entry)
        for entry in self.ignores:
            f.write("  <ignore pattern=\"%s\"/>\n" % entry)
        self.print_entries(f, "")
        f.write("</patch_data>\n")

    def print_entries(self, f, dir_name):
        for subdir_name in self.dir_tree.keys():
            f.write("  <entry name=\"%s\" kind=\"dir\" />\n" % (dir_name + subdir_name))
        for entry in self.manifest_entries:
            f.write("  <entry name=\"%s%s\"\n" % (dir_name, entry.fileName))
            f.write("         kind=\"file\" sha1_digest=\"%s\" size=\"%d\" />\n" % (entry.sha1Digest, entry.contentLength))
        for subdir_name in self.dir_tree.keys():
            self.dir_tree[subdir_name].print_entries(f, dir_name + subdir_name + "/")

class ManifestEntry:
    def __init__(self, kind, src_path, dst_path, fileName):
        # src_path is the path of the source file relative to the client_dir
        self.src_path = src_path
        # dst_path is the path of the file relative to the install dir
        self.dst_path = dst_path
        # fileName is the last component of the path to which we install
        self.fileName = fileName
        self.kind = kind
        self.sha1Digest = ""
        self.contentLength = 0

    def compute_digest(self, client_dir):
        md = sha.new()
        filename = client_dir + self.src_path
        f = file(filename, "rb")
        f.seek(0, 2)
        size = f.tell()
        f.seek(0, 0)
        while 1:
            data = f.read(4096)
            if len(data) == 0:
                break
            md.update(data)
        f.close()
        self.contentLength = size
        self.sha1Digest = md.hexdigest()

