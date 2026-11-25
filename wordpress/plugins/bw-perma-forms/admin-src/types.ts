export type Contact = {
	id: number;
	email: string;
	first_name: string;
	last_name: string;
	phone: string;
	profession: string;
	status: string;
	interests: string[];
	newsletter: string;
	source: string;
	notes: string;
	created_at: string;
	updated_at: string;
};

export type Submission = {
	id: number;
	form: string;
	interests: string[];
	message: string;
	created_at: string;
};

export type ContactDetail = Contact & {
	meta: Record< string, string >;
	submissions: Submission[];
};

export type AdminData = {
	restNs: string;
	adminUrl: string;
	modules: string[];
	/** Settings tab only for users who may change settings (administrators). */
	canManage?: boolean;
	exportUrl?: string;
	statuses?: string[];
	interests?: string[];
	newsletter?: string[];
};

declare global {
	interface Window {
		bwPermaFormsAdmin: AdminData;
	}
}
