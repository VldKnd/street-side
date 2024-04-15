'use client';
import { useState } from 'react'
import DropDownList from '@/app/components/DropDownList';
import DownloadPeriodComponent from '@/app/raw/components/DownloadPeriodComponent';
import Document from '@/app/raw/components/Document';

export default function RawDocumentsPage() {
  const [selectedClearingCompany, setSelectedClearingCompany] = useState('');
  const [selectedDocument, setSelectedDocument] = useState('');

  return (
    <div className='w-4/6'>
      <div className='relative w-full'>
        <div className='mb-3 ml-3 text-foreground-white text-base'>
          {"Select a clearing company"}
        </div>

        <div className='h-full w-full'>
          <DropDownList
            className='relative inline-block w-full bg-company-grey rounded-2xl mb-3 text-foreground-white text-base'
            elements={["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]}
            placeholder={"Click to select"}
            selectCallback={setSelectedClearingCompany}
            id={'dropdown_list'}
          />
        </div>
      </div>
      {selectedClearingCompany !== '' &&
        <div className='flex mt-3'>
          <div className="border-2 border-company-grey rounded-2xl">
            <div className="m-3">
              <div className='mb-3 ml-3 mr-3 text-foreground-white text-base'>
                {"Select a document to view"}
              </div>
              <DropDownList
                className='relative inline-block w-full bg-company-grey rounded-2xl mb-3 text-foreground-white text-base'
                elements={["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]}
                placeholder={"Click to select"}
                selectCallback={setSelectedDocument}
                id={'dropdown_list'}
              />
            </div>
          </div>
          <div className="grow" />
          <DownloadPeriodComponent />
        </div>
      }
      {(selectedClearingCompany !== '' && selectedDocument !== '') &&
        <Document />
      }
    </div>
  );
}
