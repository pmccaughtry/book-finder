import type { ReactNode } from 'react';
import Image from "next/image";

export interface Result {
    id: string;
    volumeInfo: {
        authors: string[];
        description: string;
        imageLinks: {
            smallThumbnail: string;
            thumbnail: string;
        };
        subtitle: string;
        title: string;
        [prop: string]: any;
    }
}

// export interface BookDetails {
//     authors: string;
//     description: string;
//     imageLinks: {
//         smallThumbnail: string;
//         thumbnail: string;
//     }
//     title: string;
// }

export default function Listing({ result }: { result: Result }): ReactNode {
    console.log('<Listing result={result} />:\n', result);
    const { authors, description, imageLinks, title } = result.volumeInfo;

    return (
        <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
            <h3 className="text-lg font-semibold text-gray-800 pb-4">The Pragmatic Programmer</h3>
            <img src={imageLinks.thumbnail} alt={`Book Cover - ${title}`} />
            <p className="text-gray-600 mt-2"><strong>Author(s):</strong> {authors.join(', ')}</p>
            <p className="text-gray-600 mt-2"><strong>Description:</strong> {description}</p>
        </div>
    );
}
