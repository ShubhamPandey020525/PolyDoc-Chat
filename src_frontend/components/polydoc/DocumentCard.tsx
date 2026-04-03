import { FileText, FileSpreadsheet, File, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { UploadedFile } from "@/lib/types";

interface DocumentCardProps {
  file: UploadedFile;
  onRemove: () => void;
}

const getFileIcon = (type: string) => {
  if (type.includes('pdf')) return <FileText className="h-8 w-8 text-red-400" />;
  if (type.includes('csv') || type.includes('excel') || type.includes('spreadsheet'))
    return <FileSpreadsheet className="h-8 w-8 text-green-500" />;
  return <File className="h-8 w-8 text-orange-400" />;
};

const getFileExtension = (name: string) => {
  return name.split('.').pop()?.toUpperCase() || 'FILE';
};

const formatSize = (bytes: number) => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

const DocumentCard = ({ file, onRemove }: DocumentCardProps) => {
  return (
    <div className="flex items-center gap-4 rounded-xl border border-border bg-card p-4 shadow-sm transition-all hover:shadow-md">
      <div className="flex h-14 w-14 items-center justify-center rounded-lg bg-muted">
        {getFileIcon(file.type)}
      </div>
      <div className="flex-1 min-w-0">
        <p className="truncate font-medium text-card-foreground">{file.name}</p>
        <p className="text-sm text-muted-foreground">{formatSize(file.size)}</p>
      </div>
      <Badge variant="secondary" className="bg-gradient-to-r from-orange-100 to-pink-100 text-orange-700 border-0">
        {getFileExtension(file.name)}
      </Badge>
      <button
        onClick={onRemove}
        className="rounded-lg p-1.5 text-muted-foreground transition-colors hover:bg-destructive/10 hover:text-destructive"
      >
        <X size={18} />
      </button>
    </div>
  );
};

export default DocumentCard;
