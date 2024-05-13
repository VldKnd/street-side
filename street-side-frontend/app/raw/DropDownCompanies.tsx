'use client';
import { CompanyInterface, CompanySetter } from "@/app/types/company";
import { DocumentSetterInterace } from "@/app/types/document";
import { DocumentTypeSetterInterace } from "@/app/types/document_type";
import useCompanies from "@/api/v1/useCompanies";
import { Listbox } from '@headlessui/react'

interface DropDownCompaniesInterface {
    selectedCompany : null | CompanyInterface,
    setSelectedCompany : CompanySetter,
    setSelectedDocumentType : DocumentTypeSetterInterace,
    setSelectedDocument : DocumentSetterInterace,
}

function getDateAsYMD(raw_date: string) {
  const date = new Date(Date.parse(raw_date));
  return `${date.getDate()}.${date.getMonth()+1}.${date.getFullYear()}`;
}

export function DropDownCompanies({
    selectedCompany,
    setSelectedCompany,
    setSelectedDocumentType,
    setSelectedDocument,
} : DropDownCompaniesInterface ) {
    
  const { companies, isLoading } = useCompanies();
  const stackOrder = 'z-[11]'

  if (isLoading) {
    return (
    <div className={'relative overflow-hidden animate-pulse w-full h-full text-left text-sm  inline-block w-full bg-company-grey rounded-2xl text-foreground-white pl-3 pt-3 pb-2'}>
        <p className="opacity-0">
          {". . ."}
        </p>
    </div>
    )
  }

  const onListBoxChange = (value : CompanyInterface | null) => {
    if (value !== selectedCompany) {
        setSelectedCompany(value);
        setSelectedDocumentType(null);
        setSelectedDocument(null);
      }
  }

  var sortedCompanies = [...companies];
  sortedCompanies.sort(
    (lhs, rhs) => lhs.full_name.localeCompare(rhs.full_name)
  )

  return (
    <Listbox value={selectedCompany} onChange={onListBoxChange} >
    {({ open }) => (
        <>
        <Listbox.Button className={`relative ${open ? "rounded-t-2xl" : "rounded-2xl"} ${stackOrder} w-full h-full text-left justify-between text-sm flex inline-block w-full bg-company-grey text-foreground-white pl-5 pt-3 pb-2 pr-5`}>
            <p>
              { selectedCompany ? selectedCompany.full_name : "Click to select a clearing company" }
            </p>
            { selectedCompany &&
              (
                <p className='opacity-25 justify-self-end text-sm'>
                  updated on {getDateAsYMD(selectedCompany.updated_at)}
                </p>
              )
            }
        </Listbox.Button>
        <Listbox.Options className={`absolute border-solid border border-opacity-25 border-foreground-white ${stackOrder} w-full overflow-auto rounded-b-2xl bg-company-grey text-sm text-foreground-white`}>
        {sortedCompanies.map((company: CompanyInterface) => (
            <Listbox.Option
            className={`relative ${stackOrder} pt-3 pb-2 pl-5 pr-5 justify-between cursor-default select-none hover:opacity-75 flex`}
            key={company.hash_id}
            value={company}
            >
              <p>
                {company.full_name}
              </p>
              
              <p className='opacity-25 justify-self-end text-sm'>
                updated on {getDateAsYMD(company.updated_at)}
              </p>
            </Listbox.Option>
        ))}
        </Listbox.Options>
        </>
    )}
    </Listbox>
    );
}