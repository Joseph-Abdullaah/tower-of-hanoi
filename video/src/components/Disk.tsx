import { DISK_HEIGHT, diskWidth } from "../lib/layout";
import { COLORS, diskColor } from "../lib/theme";

type DiskProps = { disk: number; disks: number; x: number; y: number };

/** One pill-shaped disk centred on (x, y). */
export const Disk: React.FC<DiskProps> = ({ disk, disks, x, y }) => {
  const width = diskWidth(disk, disks);
  const color = diskColor(disk);
  return (
    <div
      style={{
        position: "absolute",
        left: x - width / 2,
        top: y - DISK_HEIGHT / 2,
        width,
        height: DISK_HEIGHT,
        borderRadius: DISK_HEIGHT / 2,
        background: color,
        boxShadow: `inset 0 5px 0 #ffffff40, inset 0 -5px 0 #00000040, 0 0 18px ${color}55`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 20,
        lineHeight: 1,
        color: COLORS.diskText,
      }}
    >
      {disk}
    </div>
  );
};
