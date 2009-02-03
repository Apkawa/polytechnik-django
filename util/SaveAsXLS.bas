REM  *****  BASIC  *****
 ' Save document as a Microsoft Excel file Sub SaveAsExcel( cFile ) cURL = ConvertToURL( cFile ) oDoc = StarDesktop.loadComponentFromURL( cURL, "_blank", 0, (_ Array(MakePropertyValue( "Hidden", True ),))
 ' Save document as a Microsoft Excel file 

' Сохранить документ в формате Acrobat PDF.
Sub SaveAsPDF( cFile )
   cURL = ConvertToURL( cFile )
   ' Открыть документ. Мы предполагаем, что тип документа
   ' будет корректно распознан, и поэтому не указываем
   ' конкретный фильтр импорта.
   oDoc = StarDesktop.loadComponentFromURL( cURL, "_blank", 0, _
            Array(MakePropertyValue( "Hidden", True ),))

   cFile = Left( cFile, Len( cFile ) - 4 ) + ".pdf"
   cURL = ConvertToURL( cFile )
   
   ' Сохранить документ, используя фильтр экспорта.
   oDoc.storeToURL( cURL, Array(_
            MakePropertyValue( "FilterName", "writer_pdf_Export"),)
   
   oDoc.close( True )
End Sub

' Сохранить документ в формате Microsoft Word. 
Sub SaveAsDoc( cFile ) 
   ' практически совпадает с SaveAsPDF
   cURL = ConvertToURL( cFile )
   oDoc = StarDesktop.loadComponentFromURL( cURL, "_blank", 0, (_
            Array(MakePropertyValue( "Hidden", True ),))


   cFile = Left( cFile, Len( cFile ) - 4 ) + ".doc"
   cURL = ConvertToURL( cFile )
   
   oDoc.storeToURL( cURL, Array(_
            MakePropertyValue( "FilterName", "MS WinWord 6.0" ),)
   oDoc.close( True )

End Sub


Sub SaveAsXLS( cFile)
	'cFile	="/home/apkawa/Code/work/polytechnik/util/test.ods" 
   ' практически совпадает с SaveAsPDF
   cURL = ConvertToURL( cFile )
   oDoc = StarDesktop.loadComponentFromURL( cURL, "_blank", 0, (_
            Array(MakePropertyValue( "Hidden", True ),))


   cFile = Left( cFile, Len( cFile ) - 4 ) + ".xls"
   cURL = ConvertToURL( cFile )
   
   oDoc.storeToURL( cURL, Array(_
            MakePropertyValue( "FilterName", "MS Excel 97" ),)
   oDoc.close( True )

End Sub


' Сохранить документ в формате OpenOffice 2.
Sub SaveAsOOO( cFile ) 
   ' практически совпадает с SaveAsPDF
   cURL = ConvertToURL( cFile )
   oDoc = StarDesktop.loadComponentFromURL( cURL, "_blank", 0, _
            Array(MakePropertyValue( "Hidden", True ),))

   ' Расширение нового файла выбирается на основании расширения
   ' исходного файла, переведённого в нижний регистр.
   Select Case LCase(Right(cFile,3))
     Case "ppt"         ' PowerPoint file.
       cFileExt = "odp"
     Case "doc"         ' Word file.
       cFileExt = "odt"
     Case "xls"         ' Excel file.
       cFileExt = "ods"
     Case Else
       cFileExt = "xxx"
    End Select
       
   cFile = Left( cFile, Len( cFile ) - 3 ) + cFileExt
   cURL = ConvertToURL( cFile )
   
   oDoc.storeAsURL( cURL, Array() )
   oDoc.close( True )

End Sub


Function MakePropertyValue( Optional cName As String, Optional uValue ) _
   As com.sun.star.beans.PropertyValue
   Dim oPropertyValue As New com.sun.star.beans.PropertyValue
   If Not IsMissing( cName ) Then
      oPropertyValue.Name = cName
   EndIf
   If Not IsMissing( uValue ) Then
      oPropertyValue.Value = uValue
   EndIf
   MakePropertyValue() = oPropertyValue
End Function

