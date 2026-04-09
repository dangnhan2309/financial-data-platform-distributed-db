export const useQuotation = () => {
    const fetchQuotations = async () => {
        // Call API to fetch quotations
    };

    const createQuotation = async (_data: any) => {
        // Call API to create quotation
    };

    const updateQuotation = async (_id: number, _data: any) => {
        // Call API to update quotation
    };

    return {
        fetchQuotations,
        createQuotation,
        updateQuotation,
    };
};
