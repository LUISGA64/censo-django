import {SidewalkList} from '../../components/sidewalks/SidewalkList.jsx';

export function SidewalksPage() {
    return (
        <section className="mt-5 ">
            <card>
                <card-header>
                    <div className="flex">

                    </div>
                </card-header>
                <card-body>
                    <SidewalkList/>
                </card-body>
            </card>
        </section>
    );
}