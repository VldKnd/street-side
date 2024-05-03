import useAllCompanies from "@/api/v1/useCompanies";
import { CompanyInterface } from "../types/company";
import { Transition } from "@headlessui/react";

export default function InLineListOfCompanies() {
    const { companies, isLoading, isError } = useAllCompanies();

    return (
    <Transition show={!isLoading && !isError}
        enter="transition-opacity duration-500"
        enterFrom="opacity-0"
        enterTo="opacity-100"
        leave="transition-opacity duration-500"
        leaveFrom="opacity-100"
        leaveTo="opacity-0"
    >
    <div className='mt-10 mb-3 ml-3'>
      <p className='font-bold text-company-grey text-foreground-white'>
        {`Data is collected from`}
      </p>
    </div>
    <div className="flex flex-wrap justify-center content-center">
        {
            companies.map(
                (company : CompanyInterface) => {
                    return (
                    <div key={company.full_name} className={`text-base m-0.5 border-solid border-2 border-title-red text-title-red rounded-xl hover:bg-title-red hover:text-background-black`}>
                        <a className={`ml-2 mr-2`} href={company.home_url} target="_blank">
                        {company.full_name}
                        </a>
                    </div>
                    )
                }
            )
        }
    </div>
    </Transition>
    )
}