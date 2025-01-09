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
    }
}

export default function Listing({ result }: { result: Result }): ReactNode {
    const { authors, description, imageLinks, title } = result.volumeInfo;
    let thumbnail = imageLinks?.thumbnail ? imageLinks.thumbnail : 'https://placehold.co/128x161?text=Image+Not+Found';

    if (process.env.NEXT_PUBLIC_NODE_ENV === 'production' && thumbnail.includes('http:')) {
        thumbnail = thumbnail.replace('http:', 'https:');
    }

    return (
        <div className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow">
            <h3 className="text-lg font-semibold text-gray-800 pb-4">{title}</h3>
            <img src={thumbnail} alt={`Book Cover - ${title}`} />
            <p className="text-gray-600 mt-2"><strong>Author(s):</strong> {authors ? authors.join(', ') : 'Author(s) not available.'}</p>
            <p className="text-gray-600 mt-2"><strong>Description:</strong> {description ? description : 'Description not available.'}</p>
        </div>
    );
}
