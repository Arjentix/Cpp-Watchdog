#include <gtest/gtest.h>
#include "bar.h"

TEST(bar, a_char) {
    ASSERT_EQ(bar('a'), 'b');
}

TEST(bar, 8_char) {
    ASSERT_EQ(bar('8'), '9');
}
