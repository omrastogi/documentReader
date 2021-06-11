# import ghostscript
import camelot 
import fitz
import json
import argparse

def extract_data(path):
  doc = fitz.open(path)
  print(len(doc))
  final_dict={}
  for page in range(1,len(doc)):
    tables = camelot.read_pdf(path,pages=str(page),flavor='lattice')
    print(len(tables),' page number is ',page)
    # tables.export('Atradius13585973.csv', f='csv', compress=True)
    try:
      data = tables[1].df
      df=data.T
      for i in df:
        s=0
        for j in df[i]:
          if '_' in j:
            df.replace(j,j.strip(' _'),inplace=True)
      for i in df:
        s=0
        for j in df[i]:
          if j.count('\n')>=4:
            s=len(df)
          if len(j)==0 or j.lower()=='na' or 'checked' in j.lower():
            s+=1
        if s>=len(df)-1:
          df.drop(columns=[i],inplace=True)

      df=df.T

      for i in df:
        s=0
        for j in df[i]:
          if j.count('\n')>=4:
            s=len(df)
          if len(j)==0 or j.lower()=='na' or 'checked' in j.lower():
            s+=1
        if s>=len(df)-2:
          df.drop(columns=[i],inplace=True)


      if df.shape[0]>1:
        dictt={}
        for i in range(df.shape[0]):
          # print(list(df.iloc[i]))
          key=df.iloc[i][0]
          l=list(df.iloc[i][1:])
          test_list = list(filter(None, l))
          dictt[key]=test_list
          final_dict['data of page '+str(page)]=dictt

      else:
          tables = camelot.read_pdf('/content/HACKATHON_SAMPLE-converted.pdf',pages=str(page),flavor='stream')
          # print(len(tables),' page number is ',page)
          # tables.export('Atradius13585973.csv', f='csv', compress=True)
          data = tables[0].df
          # print(data)
          df=data.T
          for i in df:
            s=0
            for j in df[i]:
              if '_' in j:
                df.replace(j,j.strip(' _'),inplace=True)
          for i in df:
            s=0
            for j in df[i]:
              if j.count('\n')>=4:
                s=len(df)
              if len(j)==0 or j.lower()=='na' or 'checked' in j.lower():
                s+=1
            if s>=len(df)-1:
              df.drop(columns=[i],inplace=True)

          df=df.T

          for i in df:
            s=0
            for j in df[i]:
              if j.count('\n')>=4 or 'done' in j.lower():
                s=len(df)
              if len(j)==0 or j.lower()=='na' or 'checked' in j.lower() or 'done' in j.lower():
                s+=1
            if s>=len(df)-2:
              df.drop(columns=[i],inplace=True)
          # print(df)
          df.drop(columns=[df.columns[0]],inplace=True)
          dictt={}
          if df.shape[1]>0:
            # try:
            for i in range(df.shape[0]):
              l=list(df.iloc[i])
              l=list(filter(None, l))
              if len(l)>1:
                dictt[l[0]]=l[1:]
            final_dict['data of page '+str(page)]=dictt
            # except:
            #     print('not done')

        
    except:
      final_dict['data of page '+str(page)]='Nothing to extract in this page'

  with open("tables/data.json", "w") as outfile: 
    json.dump(final_dict, outfile)

  return final_dict


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--path', type=str, default='data\\HACKATHON_SAMPLE.pdf', help='path of the pdf file')
  opt = parser.parse_args()
  extract_data(opt.path)