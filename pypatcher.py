#!/usr/local/bin/python3

__author__ = 'Daverin Nadesan'

import sys
import yaml
import argparse

general_comments = """# Patched by {} with pypatcher

# Key Replacements
# ----------------"""
class Operation(object):
  
  def __init__(self, template_dict, patch_data):
    self.template_dict = template_dict
    self.patch_data = patch_data
    self.comments = str()

  def key_replace(self):
    self.key_replace_recurse(self.patch_data,[])
    return self.comments,yaml.dump(self.template_dict, default_flow_style = False)
  
  def key_replace_recurse(self, patch_node, list_path):
    if type(patch_node) != dict:
      destination_node = self.template_dict
      for l in list_path:
        if str(l)[0] not in ['+','-'] and destination_node.get(l) == None:
          self.comments+="# ERROR - Patch path not found \"{}\"\n".format('/'.join(list_path))
          return
        elif l == list_path[-1]: #We've reached the end of the list path
          if type(patch_node) == list:
            if str(l)[0] in ['+']:
              destination_node[l[1:]]+=(patch_node)
            elif str(l)[0] in ['-']:
              for patch_list_item in patch_node:
                destination_node[l[1:]].remove(patch_list_item)
            else:
              destination_node[l] = patch_node
          elif str(l)[0] in ['+']:
            previous_node[list_path[list_path.index(l)-1]][l[1:]] = patch_node
          else:
            destination_node[l] = patch_node
        else:
          previous_node = destination_node
          destination_node = destination_node.get(l) #Traverse through list path to find the destination node
      self.comments+="# {} = {}\n".format('/'.join(list_path),patch_node)
      return
    else:
      for child_key, child_value in patch_node.items():
        new_list_path = list(list_path)
        new_list_path.append(child_key)
        self.key_replace_recurse(child_value,new_list_path)
    

def main(args):
  parser = argparse.ArgumentParser(
      description= "echo redis.yaml | py-patcher -p patch.yaml > redis_production.yaml")
  parser.add_argument('-p', help='Patch file',
                      metavar='FILE', required=True)
  parser.add_argument('-nc', help=('Turn off comments'),
                      action='store_true', default=False, required=False)
  args = parser.parse_args()

  patch_file = args.p
  
  with open(patch_file, 'r') as ifile:
    patch_string = ifile.read()
  
  template_dicts = list(yaml.safe_load_all(sys.stdin.read()))
  patch_dicts = list(yaml.safe_load_all(patch_string))

  if len(patch_dicts)>len(template_dicts):
    print("# ERROR - Patch path not found ")
    return
  
  count = 0
  print(general_comments.format(patch_file))
  for patch_dict in patch_dicts:
    if(count>0):
      print("---") #Print yaml seperator

    template_dict = template_dicts[count]
    comments, result = process_operations(template_dict,patch_dict)
    
    if not args.nc:
      print(comments)
    print(result, end='')
    count+=1

def process_operations(template_dict,patch_dict):
  operation = Operation(template_dict,patch_dict)
  return getattr(operation, "key_replace")()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))