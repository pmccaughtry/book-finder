import type { ReactNode } from 'react';

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

export default function Listing({ result }: { result: Result }): ReactNode {
    const { authors, description, imageLinks, title } = result.volumeInfo;
    const thumbnail = imageLinks?.thumbnail ? imageLinks.thumbnail : 'https://placehold.co/128x161?text=Image+Not+Found';

    return (
        <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
            <h3 className="text-lg font-semibold text-gray-800 pb-4">The Pragmatic Programmer</h3>
            <img src={thumbnail} alt={`Book Cover - ${title}`} />
            <p className="text-gray-600 mt-2"><strong>Author(s):</strong> {authors ? authors.join(', ') : 'Author(s) not available.'}</p>
            <p className="text-gray-600 mt-2"><strong>Description:</strong> {description ? description : 'Description not available.'}</p>
        </div>
    );
}
