import type { NextApiRequest, NextApiResponse } from "next";

type SearchTerms = {
    terms: string;
};

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<SearchTerms>,
) {
    res.status(200).json({ terms: "John Doe" });
}
