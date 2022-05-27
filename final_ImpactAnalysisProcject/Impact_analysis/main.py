
class Container:
    _element_positions = []
    _copybook_impacts = []
    _move_static_impacts = []
    _move_dynamic_impacts = []
    _call_static_impacts = []
    _call_dynamic_impacts = []
    _perform_impacts = []
    _procs_impacts = []
    _full_data=[]
    _is_all_data,_is_copybook,_is_static=False,False,False
    _is_dynamic,_is_move,_is_call=False,False,False
    _is_perform = False
    _is_procs = False
    
    #initializing the class
    def __init__(self,copy,static,move,call,dynamic,procs):
        self._is_call = call
        self._is_copybook = copy
        self._is_dynamic = dynamic
        self._is_static = static
        self._is_move = move
        self._is_procs = procs
    
    #getting the indexes of elements and name of the elements into the list
    def get_Elements(self,data):
        for line in range(len(data)):
            if "ELEMENT" in data[line]:
                #print(data[line],line)
                self._element_positions.append([line,data[line].split()[-1]])
                
    # this function is used to print the data            
    def print_data(self,data):
        for i in list(set(data)):
            print(i)
    
    #copying the impacted lines
    def copy_Data(self,line):
        self._full_data.append(line)
        
            
    def do_ImpactAnalysis(self,data):
        for i in range(len(self._element_positions)-1):
            
            #getting the first and last indexes of elements
            first,last = self._element_positions[i],self._element_positions[i+1]
            
            #iterating the element based on the indexes
            print(first[0],last[0],first[1])
            for j in range(first[0],last[0]):
                #print(data[j])
                #print(j)
                if "ELEMENT" in data[j]:
                   self.copy_Data(data[j])


                if "COPY" in data[j]:
                    self._copybook_impacts.append(first[1])
                    self.copy_Data(data[j])
                if "MOVE " in data[j]:
                    if "MOVE '" in data[j]:
                        self._move_static_impacts.append(first[1])
                    else:
                        self._move_dynamic_impacts.append(first[1])
                    self.copy_Data(data[j])
                if "CALL " in data[j]:
                    if "CALL '" in data[j]:
                        self._call_static_impacts.append(first[1])
                    else:
                        self._call_dynamic_impacts.append(first[1])
                    self.copy_Data(data[j])
                if "PERFORM" in data[j]:
                    self._perform_impacts.append(first[1])
                    self.copy_Data(data[j])
                    
                if "EXEC " in data[j]:
                    
                    self._procs_impacts.append(first[1])
                    self.copy_Data(data[j])
                    
    #this method converts the list data into string                
    def convert_list_to_string(self,data):
        new_data = []
        for i in data:
            if not i in new_data:
                new_data.append(i)
        string = "\n".join(map(str,new_data))
        return string
    #this method is used to write headers in the file                
    def print_headers(self,file,header_name):
        stars = "*"*30
        file.write("\n"+stars+"\n")
        file.write(header_name+"\n")
        
    #this function will dump all the impacted data into the impacted file                
    def _impact_file(self):
        try:
            impact_file = open("outputfiles/impactfile1.txt","r+")
            impact_file.truncate(0)
        except:    
            impact_file = open("outputfiles/impactfile1.txt","w+")
        for i in self._full_data:
            impact_file.write(i+"\n")
            
        impact_file.close()
     
    #this function will generate the output file with impacted elements based on 
    #  requirement of the user
    def generating_output_file(self):
        
        #creating a file
        output_file = open("outputfiles/output1.txt","w+")
        
        #writing copybook impacted elements 
        if self._is_copybook:
            self.print_headers(output_file,"COPYBOOK IMPACTS")
            output_file.write(self.convert_list_to_string(self._copybook_impacts))
        
            
        if self._is_call:
            self.print_headers(output_file,"CALL IMPACTS")
            if self._is_static:
                output_file.write(self.convert_list_to_string(self._call_static_impacts))
            elif self._is_dynamic:
                output_file.write(self.convert_list_to_string(self._call_dynamic_impacts))
                
        if self._is_move:
            self.print_headers(output_file,"MOVE IMPACTS")
            if self._is_static:
                output_file.write(self.convert_list_to_string(self._move_static_impacts))
            elif self._is_dynamic:
                output_file.write(self.convert_list_to_string(self._move_dynamic_impacts))
                
        if self._is_perform:
            self.print_headers(output_file,"PERFORM IMPACTS")
            output_file.write(self.convert_list_to_string(self._perform_impacts))
            
        if self._is_procs:
            self.print_headers(output_file, "PROCS IMPACTS")
            output_file.write(self.convert_list_to_string(self._procs_impacts))
        
        output_file.close()
            
        
        
            
        
            
            
                    
                
                    
        
                
    
                
                
    
        

class Main:
    
    data_to_pass = {}
    #getting the data
    def sent_file(self,inputfile,copy,static,move,call,dynamic,im_ele,im_file,procs):
        self.inputfile = inputfile
        obj = Container(copy,static,move,call,dynamic,procs)
        try:
            datas = self.inputfile.read()
            datas = datas.decode('utf8',errors='ignore').split("\n")
        except:
            f = open(self.inputfile,'r')
            datas = f.read()
            datas = datas.split("\n")

        
        data =[]
        
        #removing the comments in the XDC file
        for i in datas:
            if not "*" in i:
                data.append(i)
        #getting the index and Element name
        obj.get_Elements(data)
        last_element_index = len(data)-1
        obj._element_positions.append([last_element_index,"BOTTOM"])
        
        #performing impact analysis
        obj.do_ImpactAnalysis(data)
        
        
        #sending data to javascript
        if im_ele:
            obj.generating_output_file()
            self.data_to_pass["im_ele"] = "yes"
        else:
            self.data_to_pass["im_ele"] = "no"
            
            
        if im_file:
            obj._impact_file()
            self.data_to_pass["im_file"] = "yes"
        else:
            self.data_to_pass["im_file"] = "no"
            
        del obj
            
        


        

        
        
        
        
        
        

