import { Button } from 'primereact/button';

import { TieredMenu } from 'primereact/tieredmenu';
        
import React, { useRef } from 'react';

// Define types for menu items
interface MenuItem {
    label: string;
    icon?: string;
    items?: MenuItem[];
    separator?: boolean;
}

export const MenuAcciones = () => {
    const menu = useRef<any>(null);

    const items: MenuItem[] = [
        {
            label: 'File',
            icon: 'pi pi-file',
            items: [
                {
                    label: 'New',
                    icon: 'pi pi-plus',
                    items: [
                        { label: 'Document', icon: 'pi pi-file' },
                        { label: 'Image', icon: 'pi pi-image' },
                        { label: 'Video', icon: 'pi pi-video' },
                    ]
                },
                { label: 'Open', icon: 'pi pi-folder-open' },
                { label: 'Print', icon: 'pi pi-print' }
            ]
        },
        {
            label: 'Edit',
            icon: 'pi pi-file-edit',
            items: [
                { label: 'Copy', icon: 'pi pi-copy' },
                { label: 'Delete', icon: 'pi pi-times' }
            ]
        },
        { label: 'Search', icon: 'pi pi-search' },
        {
            label: 'Share',
            icon: 'pi pi-share-alt',
            items: [
                { label: 'Slack', icon: 'pi pi-slack' },
                { label: 'Whatsapp', icon: 'pi pi-whatsapp' }
            ]
        }
    ];

    return (
        <div className="card flex justify-content-center">
            {/* <TieredMenu model={items} popup ref={menu} breakpoint="767px" />
            <Button label="Show" onClick={(e) => menu.current.toggle(e)} /> */}
        </div>
    );
};
