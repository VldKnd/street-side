'use client';
import { useState } from 'react'
import { useClickAway } from "@uidotdev/usehooks";

import DocumentSelector from '@/app/raw/components/DocumentSelector';
import DownloadPeriodComponent from '@/app/raw/components/DownloadPeriodComponent';
import Document from '@/app/raw/components/Document';

type SelectionCallback = (selected: string) => void

function DropDownList(
  { className, elements, placeholder, id, selectCallback }:
    { className: string, elements: string[], placeholder: string, id: string, selectCallback?: SelectionCallback }
) {

  if (typeof selectCallback === 'undefined') {
    selectCallback = (selected: string) => { }
  }

  const [isOpen, setIsOpen] = useState(false)
  const [selected, setSelected] = useState('')

  const ref = useClickAway(() => {
    setIsOpen(false)
  });

  return (
    <div className={`${className}`} id={id} ref={ref}>
      <div>
        <button onClick={() => setIsOpen(!isOpen)} className='w-full h-full text-left text-base'>
          <p className='ml-4 mt-3 mb-2'>
            {selected == '' ? placeholder : selected}
          </p>
        </button>
      </div>
      {isOpen &&
        <div className='absolute z-10 border bg-company-grey border-foreground-white rounded-b-2xl rounded-t-2xl origin-top-right w-full mt-2 max-h-64 overflow-auto'>
          <ul>
            {elements.map((element, index) => {
              return (
                <li
                  onClick={() => { setIsOpen(!isOpen); setSelected(element); selectCallback(element); }}
                  className={
                    `flex hover:opacity-50 bg-company-grey ${index == (elements.length - 1) ? "rounded-b-2xl" : ""} ${index == 0 ? "rounded-t-2xl" : ""}`}>
                  <button onClick={() => setIsOpen(!isOpen)} className='w-full h-full text-left text-base'>
                    <p className='ml-4 mt-3 mb-2'>
                      {element}
                    </p>
                  </button>
                </li>
              )
            })}
          </ul>
        </div>
      }
    </div>
  )
}


export default async function RawDocumentsPage() {
  const [selectedClearingCompany, setSelectedClearingCompany] = useState('');
  const [selectedDocument, setSelectedDocument] = useState('');

  await new Promise(resolve => setTimeout(resolve, 1000))

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
