from google.auth.transport.requests import Request

from googleapiclient.discovery import build

from google.oauth2 import service_account

import json 

class GoogleClient():

    def __init__(self, creds_path, project=None):
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                  'https://www.googleapis.com/auth/documents.readonly'
                 ]
        self.project = project
        self.credentials = service_account.Credentials.from_service_account_file(creds_path, scopes = scopes)

    def build_service(self, service_type):
        if service_type == "sheets":
            return build(service_type, "v4", credentials=self.credentials)
        elif service_type == "docs":
            return build(service_type, "v1", credentials=self.credentials)
        else:
            raise Exception("Service type not supported")
    
    def get_sheets(self,spreadSheetId, range, major_dimensions=None):
        service = self.build_service("sheets")
        request = service.spreadsheets().values().get(spreadsheetId=spreadSheetId, range=range, majorDimension = major_dimensions)
        return request.execute()
    
    def get_documents(self, docId):
        service = self.build_service("docs")
        request = service.documents().get(documentId=docId)
        return request.execute()

    @staticmethod
    def read_paragraph_element(element):
    
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    @staticmethod
    def read_structural_elements(elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += GoogleClient.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += read_structural_elements(cell.get('content'))
            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += read_structural_elements(toc.get('content'))
        return text


if __name__== "__main__":
    client = GoogleClient("keys\yosimontesdeoca-89f3bd9eed1d.json")

    #print(client.get_sheets("16iQPSnZ5Ypkm5Jw0moIEz2-pzTflcYUpCCjGrTvPtVo", "A4:BS5")['values'])

    #print(client.get_documents("1kGP3cm2yvmrqxDwgTfzLLvQEBfq6MGcTkmLIWIT4Lz0").get('body'))

    print(client.read_structural_elements(client.get_documents("1kGP3cm2yvmrqxDwgTfzLLvQEBfq6MGcTkmLIWIT4Lz0").get('body').get('content')))

    


        

