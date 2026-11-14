#!/usr/bin/env bash
# Rút gọn mô hình Poly Haven (giảm tam giác) và gói mỗi mô hình thành một file .glb để engine nạp nhanh.
#   bash video3d/chat_lieu/gon.sh <thư mục có mo_hinh/> <đường dẫn gltf-transform>
set -e
D="$1"; GT="${2:-gltf-transform}"
declare -A RATIO=([island_tree_01]=0.018 [island_tree_02]=0.025 [island_tree_03]=0.014 [pachira_aquatica_01]=0.15 [boulder_01]=0.08 [grass_medium_01]=0.4)
for f in "$D"/mo_hinh/*/*.gltf; do
  m=$(basename "$f" .gltf); r=${RATIO[$m]:-1}
  if [ "$r" = 1 ]; then "$GT" copy "$f" "$D/$m.glb"; else "$GT" simplify "$f" "$D/$m.glb" --ratio "$r" --error 0.02; fi
done
rm -rf "$D/mo_hinh"; ls -la "$D"/*.glb
